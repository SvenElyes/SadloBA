try:
    from paraview.util.vtkAlgorithm import *
    import paraview.detail.pythonalgorithm as pvdetail

    __paraview = True

except ImportError:
    __paraview = False

# check if vtkmodules exists, otherwise create an alias
try:
    import vtkmodules
except ImportError:
    import vtk
    import sys

    sys.modules["vtkmodules"] = sys.modules["vtk"]

if __paraview:
    import inspect
    import html

    def smdomain_enumeration(labels, values, **kwargs):
        attrs = {"type": "EnumerationDomain", "name": "enum"}
        attrs.update(kwargs)

        def generate(func, attrs):
            type_xmls = []
            for text, value in zip(labels, values):
                type_xmls.append(
                    pvdetail._generate_xml(
                        {"type": "Entry", "text": text, "value": value}, []
                    )
                )
            smdomain._append_xml(func, pvdetail._generate_xml(attrs, type_xmls))

        return pvdetail._create_decorator(attrs, generate_xml_func=generate)

    def smdomain_boolean(**kwargs):
        attrs = {"type": "BooleanDomain", "name": "bool"}
        attrs.update(kwargs)
        return pvdetail._create_decorator(
            attrs, generate_xml_func=smdomain._generate_xml
        )

    def smdomain_inputarray(name="input_array", attribute_type="any", **kwargs):
        attrs = {
            "type": "InputArrayDomain",
            "name": name,
            "attribute_type": attribute_type,
        }
        attrs.update(kwargs)
        return pvdetail._create_decorator(
            attrs, generate_xml_func=smdomain._generate_xml
        )

    smdomain.enumeration = staticmethod(smdomain_enumeration)
    smdomain.boolean = staticmethod(smdomain_boolean)
    smdomain.inputarray = staticmethod(smdomain_inputarray)

    def smproperty_outputport(name, index="0", **kwargs):
        attrs = {"type": "OutputPort", "name": name, "index": index}
        attrs.update(kwargs)
        return pvdetail._create_decorator(
            attrs, generate_xml_func=smproperty._generate_xml
        )

    def smproperty_inputarray(
        label,
        idx=0,
        input_domain_name="input_array",
        input_name="Input",
        none_string=None,
        attribute_type="Scalars",
        **kwargs
    ):
        def generate(func, attrs):
            xml = """<StringVectorProperty
                        name="SelectInputScalars{idx}"
                        label="{label}"
                        command="{command}"
                        default_values="{idx}"
                        number_of_elements="5"
                        element_types="0 0 0 0 2"
                        animateable="0">
                        <ArrayListDomain
                          name="array_list"
                          attribute_type="{attribute_type}"
                          input_domain_name="{input_domain_name}"
                          {none_property}>
                          <RequiredProperties>
                            <Property
                              name="{input_name}"
                              function="Input" />
                          </RequiredProperties>
                        </ArrayListDomain>
                      </StringVectorProperty>
            """.format(
                **attrs
            )
            smproperty._append_xml(func, xml)

        attrs = {
            "idx": idx,
            "label": label,
            "input_domain_name": input_domain_name,
            "input_name": input_name,
            "none_property": 'none_string="{}"'.format(none_string)
            if none_string
            else "",
            "attribute_type": attribute_type,
        }
        attrs.update(kwargs)
        return pvdetail._create_decorator(
            attrs,
            update_func=smproperty._update_property_defaults,
            generate_xml_func=generate,
        )

    smproperty.outputport = staticmethod(smproperty_outputport)
    smproperty.inputarray = staticmethod(smproperty_inputarray)

    def smhint_menu(menu):
        attrs = {"type": "ShowInMenu", "category": menu}
        return pvdetail._create_decorator(attrs, generate_xml_func=smhint._generate_xml)

    def smhint_replace_input(replace):
        attrs = {"type": "Visibility", "replace_input": replace}
        return pvdetail._create_decorator(attrs, generate_xml_func=smhint._generate_xml)

    def smhint_widget_visibility(property_name, value):
        return smhint.xml(
            '<PropertyWidgetDecorator mode="visibility" property="{}" type="GenericDecorator" value="{}"/>'.format(
                property_name, value
            )
        )

    def smhint_widget_multiline(highlight_syntax=False):
        return smhint.xml(
            '<Widget syntax="python" type="multi_line"/>'
            if highlight_syntax
            else '<Widget type="multi_line"/>'
        )

    smhint.menu = staticmethod(smhint_menu)
    smhint.replace_input = staticmethod(smhint_replace_input)
    smhint.widget_visibility = staticmethod(smhint_widget_visibility)
    smhint.widget_multiline = staticmethod(smhint_widget_multiline)

    def __patch_generate_xml(classobj, attrs):
        nested_xmls = []

        classobj = pvdetail._undecorate(classobj)
        if hasattr(classobj, "_pvsm_property_xmls"):
            val = getattr(classobj, "_pvsm_property_xmls")
            if type(val) == type([]):
                nested_xmls += val
            else:
                nested_xmls.append(val)

        prop_xmls_dict = {}
        prop_ordering = {}
        for pname, val in classobj.__dict__.items():
            val = pvdetail._undecorate(val)
            if callable(val) and hasattr(val, "_pvsm_property_xmls"):
                pxmls = getattr(val, "_pvsm_property_xmls")
                if len(pxmls) > 1:
                    raise RuntimeError(
                        "Multiple property defintions on the same"
                        "method are not supported."
                    )
                prop_xmls_dict[pname] = pxmls[0]
                prop_ordering[pname] = val.__code__.co_firstlineno

        # sort properties by the line numbers of their functions
        nested_xmls += [
            prop_xmls_dict[key]
            for key in sorted(prop_xmls_dict.keys(), key=prop_ordering.get)
        ]

        if attrs.get("support_reload", True):
            nested_xmls.insert(
                0,
                """
                <Property name="Reload Python Module" panel_widget="command_button">
                    <Documentation>Reload the Python module.</Documentation>
                </Property>""",
            )

        if classobj.__doc__:
            nested_xmls.append(
                pvdetail._generate_xml(
                    {"type": "Documentation"}, [html.escape(classobj.__doc__)]
                )
            )

        if hasattr(classobj, "_pvsm_hints_xmls"):
            hints = [h for h in classobj._pvsm_hints_xmls]
            nested_xmls.append(pvdetail._generate_xml({"type": "Hints"}, hints))

        proxyxml = pvdetail._generate_xml(attrs, nested_xmls)
        groupxml = pvdetail._generate_xml(
            {"type": "ProxyGroup", "name": attrs.get("group")}, [proxyxml]
        )
        smconfig = pvdetail._generate_xml(
            {"type": "ServerManagerConfiguration"}, [groupxml]
        )
        setattr(classobj, "_pvsm_proxy_xml", smconfig)

    smproxy._generate_xml = staticmethod(__patch_generate_xml)

    def __patch_smproperty_generate_xml(func, attrs):
        nested_xmls = []
        if hasattr(func, "_pvsm_domain_xmls"):
            for d in func._pvsm_domain_xmls:
                nested_xmls.append(d)
            delattr(func, "_pvsm_domain_xmls")
        if hasattr(func, "_pvsm_hints_xmls"):
            hints = []
            for h in func._pvsm_hints_xmls:
                hints.append(h)
            nested_xmls.append(pvdetail._generate_xml({"type": "Hints"}, hints))
            delattr(func, "_pvsm_hints_xmls")
        if not inspect.isclass(func) and func.__doc__:
            nested_xmls.append(
                pvdetail._generate_xml(
                    {"type": "Documentation"}, [html.escape(func.__doc__)]
                )
            )

        pxml = pvdetail._generate_xml(attrs, nested_xmls)
        smproperty._append_xml(func, pxml)

    smproperty._generate_xml = staticmethod(__patch_smproperty_generate_xml)

    # backward compatibility to ParaView v5.7.0
    import sys
    import paraview.modules

    try:
        import paraview.modules.vtkPVVTKExtensionsFiltersPython
    except ImportError:
        import paraview.modules.vtkPVClientServerCorePythonPython

        sys.modules["paraview.modules.vtkPVVTKExtensionsFiltersPython"] = sys.modules[
            "paraview.modules.vtkPVClientServerCorePythonPython"
        ]
    try:
        import paraview.modules.vtkPVVTKExtensionsFiltersGeneral
    except ImportError:
        import paraview.modules.vtkPVVTKExtensionsDefaultPython

        sys.modules["paraview.modules.vtkPVVTKExtensionsFiltersGeneral"] = sys.modules[
            "paraview.modules.vtkPVVTKExtensionsDefaultPython"
        ]
else:
    # no paraview module: mock away all paraview-related functions

    from functools import wraps

    def _mock_method(*args, **kwargs):
        def _mock_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return _mock_decorator

    class _mock_class:
        def __getattr__(self, name):
            return _mock_method

    smproxy = smproperty = smhint = smdomain = _mock_class()
    smdomain_enumeration = smdomain_boolean = smdomain_inputarray = _mock_method
    smproperty_inputarray = _mock_method
    smhint_menu = (
        smhint_replace_input
    ) = smhint_widget_visibility = smhint_widget_multiline = _mock_method

    from vtkmodules.util.vtkAlgorithm import *
