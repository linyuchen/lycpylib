# -*- coding: UTF8 -*-

from xml.dom import minidom


class XmlParser(object):
    """
    dom: xml.dom
    """

    def __init__(self, path=None, xml_data=None):
        """

        :param path: str
        :param xml_data: str
        """
        if path:
            self.dom = minidom.parse(path)
            self.root = self.dom.childNodes[0]
        elif xml_data:
            self.dom = minidom.parseString(xml_data)
            self.root = self.dom.childNodes[0]
        else:
            self.dom = minidom.Document()
            self.root = self.dom.createElement("xml")
            self.dom.appendChild(self.root)

    def add_element(self, tag_name, text=None, attrs={}, is_cdata=False, parent_element=None):
        """

        :param tag_name:
        :param text:
        :param attrs:
        :param is_cdata:
        :param parent_element:
        :return: element
        """
        child_element = self.dom.createElement(tag_name)
        text_node = minidom.Text()
        if text:
            if is_cdata:
                text_node = minidom.CDATASection()
            text_node.data = text
            child_element.appendChild(text_node)
        for key, value in attrs.items():
            child_element.setAttribute(key, value)
        p = parent_element
        if not p:
            p = self.root

        p.appendChild(child_element)
        return child_element

    def get_element(self, tag_name, parent_element=None):
        p = parent_element
        if not p:
            p = self.dom

        return self.dom.getElementsByTagName(tag_name)

    def get_element_text(self, tag_name, parent_element=None):
        child_elements = self.get_element(tag_name, parent_element)
        if child_elements:
            child_element = child_elements[0]
        else:
            return ""
        text_node = child_element.firstChild
        if isinstance(text_node, (minidom.Text, minidom.CDATASection)):
            return text_node.data
        else:
            return ""

    def to_string(self, encoding=None):
        return self.dom.toxml(encoding)

