# system librearies
import subprocess
from datetime import datetime

# Third-party libraries

# django modules

# django apps

# current app modules


# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)


"""
A collection of tools around :doc:`multi-table inheritance </dev/mti>`.
"""
from builtins import str
import logging

logger = logging.getLogger(__name__)

from django.db import models
from django.db import router
# from django.db.models.deletion import Collector
from django.db.models.deletion import Collector, DO_NOTHING
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class ChildCollector(Collector):
    """
    A Collector that does not delete the MTI parents.
    """

    def collect(self, objs, source=None, nullable=False, collect_related=True,
                source_attr=None, reverse_dependency=False):
        # modified copy of django.db.models.deletion.Collector.collect()
        # changes:
        # DOES NOT Recursively collect concrete model's parent models.
        # calls get_all_related_objects() with local_only=True

        if self.can_fast_delete(objs):
            self.fast_deletes.append(objs)
            return
        new_objs = self.add(objs, source, nullable,
                            reverse_dependency=reverse_dependency)
        if not new_objs:
            return

        model = new_objs[0].__class__

        if collect_related:

            related_objects = [
                f for f in model._meta.get_fields(include_hidden=True)
                if (f.one_to_many or f.one_to_one)
                and f.auto_created and not f.concrete
                and f.model is model  ## local_only
                ]

            # Before Django 1.10 we had:
            # related_objects = model._meta.get_all_related_objects(
            #         include_hidden=True, include_proxy_eq=True,
            #         local_only=True)

            for related in related_objects:
                field = related.field
                if field.rel.on_delete == DO_NOTHING:
                    continue
                sub_objs = self.related_objects(related, new_objs)
                if self.can_fast_delete(sub_objs, from_field=field):
                    self.fast_deletes.append(sub_objs)
                elif sub_objs:
                    field.rel.on_delete(self, field, sub_objs, self.using)
            for field in model._meta.virtual_fields:
                if hasattr(field, 'bulk_related_objects'):
                    # Its something like generic foreign key.
                    sub_objs = field.bulk_related_objects(new_objs, self.using)
                    self.collect(sub_objs,
                                 source=model,
                                 source_attr=field.rel.related_name,
                                 nullable=True)


def get_child(obj, child_model):
    if obj.pk is not None:
        try:
            return child_model.objects.get(pk=obj.pk)
        except child_model.DoesNotExist:
            # logger.warning(
            #     "No mti child %s in %s",
            #     obj.pk, child_model.objects.all().query)
            return None


def delete_child(obj, child_model, ar=None, using=None):
    """
    Delete the `child_model` instance related to `obj` without
    deleting the parent `obj` itself.
    """
    # logger.info(u"delete_child %s from %s",child_model.__name__,obj)
    using = using or router.db_for_write(obj.__class__, instance=obj)
    child = get_child(obj, child_model)
    if child is None:
        raise Exception("%s has no child in %s" % (obj, child_model.__name__))

    # msg = child.disable_delete(ar)
    ignore_models = set()
    # for m in models_by_base(obj.__class__):
    #     ignore_models.remove(child_model)
    msg = child._lino_ddh.disable_delete_on_object(
        obj, ignore_models)
    if msg:
        raise ValidationError(msg)
    # logger.debug(u"Delete child %s from %s",child_model.__name__,obj)

    # 20160720 TODO: Django has added the keep_parents argument, and
    # we should use this before Django 1.10 but this still seems to
    # delete objects that are related to parents. So we sill cannot
    # use it.
    if True:
        collector = ChildCollector(using=using)
        collector.collect([child])
        # raise Exception(repr(collector.data))
        # model = obj.__class__

        # remove the collected MTI parents so they are not deleted
        # (this idea didnt work: yes the parents were saved, but not
        # their related objects).

        # concrete_model = child_model._meta.concrete_model
        # for ptr in six.itervalues(concrete_model._meta.parents):
        #     if ptr:
        #         # raise Exception(repr(ptr.rel.model))
        #         del collector.data[ptr.rel.model]

    else:
        collector = Collector(using=using)
        collector.collect([child], source=obj.__class__,
                          nullable=True, keep_parents=True)
    collector.delete()

    # ~ setattr(obj,child_model.__name__.lower(),None)
    # ~ delattr(obj,child_model.__name__.lower())

    # TODO: unchecking e.g. Company.is_courseprovider deletes the
    # child when saving the form, but the response to the PUT returns
    # still a True value because it works on the same memory instance
    # (`obj`).  User sees the effect only after clicking the refresh
    # button.  Fortunately there's no problem if the user unchecks the
    # field and saves the form a second time.


def insert_child(obj, child_model, full_clean=False, **attrs):
    """Create and save an instance of `child_model` from existing `obj`.
    If `full_clean` is True, call full_clean on the newly created
    object. Default is `False` because this was the historic
    behaviour.
    """
    # ~ assert child_model != obj.__class__
    # ~ if child_model == obj.__class__:
    # ~ raise ValidationError(
    # ~ "A %s cannot be parent for itself" %
    # ~ obj.__class__.__name__)
    parent_link_field = child_model._meta.parents.get(obj.__class__, None)
    if parent_link_field is None:
        raise ValidationError(str("A %s cannot be parent for a %s" % (
            obj.__class__.__name__, child_model.__name__)))
    attrs[parent_link_field.name] = obj
    # ~ for pm,pf in child_model._meta.parents.items(): # pm : parent model, pf : parent link field
    # ~ attrs[pf.name] = obj
    # ~ attrs["%s_ptr" % obj.__class__.__name__.lower()] = obj
    # if AFTER17:
    #   fields_list = obj._meta.concrete_fields
    # else:

    fields_list = obj._meta.fields

    for field in fields_list:
        attrs[field.name] = getattr(obj, field.name)
    new_obj = child_model(**attrs)
    # ~ logger.info("20120830 insert_child %s",obj2str(new_obj))

    new_obj.save()

    # on_add_child.send(sender=obj, child=new_obj)
    if full_clean:
        try:
            new_obj.full_clean()
            new_obj.save()
        except ValidationError as e:
            msg = obj.error2str(e)
            raise ValidationError(
                _("Problem while inserting %(child)s "
                  "child of %(parent)s: %(message)s") %
                dict(child=child_model.__name__,
                     parent=obj.__class__.__name__,
                     message=msg))
    return new_obj


def mtichild(p, model, **kw):
    """Create an MTI child, optionally set some attributes, save it to the
    database and then return the new database object.
    """
    c = insert_child(p, model)
    for k, v in kw.items():
        setattr(c, k, v)
    c.full_clean()
    c.save()
    return model.objects.get(pk=p.pk)


# ~ def insert_child_and_save(obj,child_model,**attrs):
# ~ """
# ~ Insert (create) and save a `child_model` instance of existing `obj`.
# ~ """
# ~ obj = insert_child(obj,child_model,**attrs)
# ~ obj.save()
# ~ return obj




def get_git_changeset(absolute_path):
    repo_dir = absolute_path
    git_show = subprocess.Popen(
        'git show --pretty=format:%ct --quiet HEAD',
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True, cwd=repo_dir, universal_newlines=True,
    )
    timestamp = git_show.communicate()[0].partition('\n')[0]
    try:
        timestamp = datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return ""
    changeset = timestamp.strftime('%Y%m%d%H%M%S')
    return changeset


