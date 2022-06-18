"""direct copy from https://vcgitlab.iwr.uni-heidelberg.de/prtl/prtl/-/blob/master/python/pyprtl/util/arrays.py"""

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.numpy_interface import dataset_adapter as dsa


def field_from_association(dataobject, field, numpy=True):
    if numpy and not isinstance(dataobject, dsa.VTKObjectWrapper):
        dataobject = dsa.WrapDataObject(dataobject)
    if field == vtkDataObject.FIELD_ASSOCIATION_POINTS:
        return dataobject.PointData if numpy else dataobject.GetPointData()
    elif field == vtkDataObject.FIELD_ASSOCIATION_CELLS:
        return dataobject.CellData if numpy else dataobject.GetCellData()
    elif field == vtkDataObject.FIELD_ASSOCIATION_NONE:
        return dataobject.FieldData if numpy else dataobject.GetFieldData()
    else:  # remaining field associations not implemented
        raise ValueError()


def get_array(dataobject, field, name, numpy=True, return_none_array=False):
    data_field = field_from_association(dataobject, field, numpy)
    if numpy:
        array = data_field[name]
    else:
        array = data_field.GetArray(name)
    if not return_none_array and array is dsa.NoneArray:
        return None
    return array


def find_array(dataobject, name, numpy=True):
    for field in [
        vtkDataObject.FIELD_ASSOCIATION_POINTS,
        vtkDataObject.FIELD_ASSOCIATION_CELLS,
        vtkDataObject.FIELD_ASSOCIATION_NONE,
    ]:
        array = get_array(dataobject, field, name, numpy=numpy, return_none_array=False)
        if array is not None:
            return array, field
    return None, None
