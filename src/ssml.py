#!/usr/bin/env python3
"""
SSML (Speech Synthesis Markup Language) is a subset of XML specifically
designed for controlling synthesis. You can see examples of how the SSML
should be parsed in the unit tests below.
"""

#
# DO NOT USE CHATGPT, COPILOT, OR ANY AI CODING ASSISTANTS.
# Conventional auto-complete and Intellisense are allowed.
#
# DO NOT USE ANY PRE-EXISTING XML PARSERS FOR THIS TASK - lxml, ElementTree, etc.
# You may use online references to understand the SSML specification, but DO NOT read
# online references for implementing an XML/SSML parser.
#


from dataclasses import dataclass
from typing import List, Union, Dict
import re

SSMLNode = Union["SSMLText", "SSMLTag"]


@dataclass
class SSMLTag:
    name: str
    attributes: dict[str, str]
    children: list[SSMLNode]

    def __init__(
        self, name: str, attributes: Dict[str, str] = {}, children: List[SSMLNode] = []
    ):
        self.name = name
        self.attributes = attributes
        self.children = children


@dataclass
class SSMLText:
    text: str

    def __init__(self, text: str):
        self.text = text

# def _parse_element(element: ET.Element) -> SSMLTag: 
#     children: List[SSMLNode] = []

#     if element.text and element.text.strip():
#         children.append(SSMLText(element.text.strip()))

#     for child in element:
#         children.append(_parse_element(child))

#         if child.tail and child.tail.strip():
#             children.append(SSMLText(child.tail.strip()))
#     return SSMLTag(
#         name=element.tag,
#         attributes=dict(element.attrib),
#         children=children
        # )

TAG_REGEX = re.compile(r"<(/?)(\w+)([^>]*)>|([^<]+)")

def tokenize(ssml: str):
    tokens = []

    for match in TAG_REGEX.finditer(ssml):
        if match.group(4):
            text = tokens.append({"type": "text", "value": text})
        else:
            closing = match.group(1) == "/"
            tag = match.group(2)
            attr_string = match.group(3).strip()
            attrs = {}
            if attr_string:
                attr_pairs = re.findall(r'(\w+)="([^"]+)"', attr_string)
                attrs = dict(attr_pairs)
            if closing:
                tokens.append({"type": "end", "name": tag})
            else:
                tokens.append({"type": "start", "name": tag, "attributes": attrs})
    return tokens

VALID_TAGS = {"speak", "p"}
VALID_ATTRIBUTES = {
    "speak": set(),
    "p": set(),
}

def build_tree(tokens):
    stack = []
    root = None

    for token in tokens:
        if token["type"] == "start":
            node = SSMLTag(token["name"], token["attributes"], [])
            if stack:
                stack[-1].children.append(node)
            else:
                root = node
            stack.append(node)
        elif token["type"] == "end":
            stack.pop()

        elif token["type"] == "text":
            if stack:
                stack[-1].children.append(SSMLText(token["value"]))
    return root

def parseSSML(ssml: str) -> SSMLNode:
    # TODO: implement this function
    ssml = ssml.strip()

    if not ssml.startswith("<speak>"):
        raise Exception("Missing <speak> root tag")
    
    tokens = tokenize(ssml)
    stack: List[SSMLTag] = []

    for token in tokens:
        if token["type"] == "start":
            tag = token["name"]
            attrs = token["attributes"]
            if tag not in VALID_TAGS:
                raise Exception(f"Invalid tag: {tag}")
            
            for attr in attrs:
                if attr not in VALID_ATTRIBUTES[tag]:
                    raise Exception(f"Invalid attribute {attr} for {tag}")
            
            node = SSMLTag(name=tag, attributes=attrs, children=[])

            if stack:
                stack[-1].children.append(node)
            
                stack.append(node)
            elif token["type"] == "end":
                if not stack or stack[-1].name != token["name"]:
                    raise Exception("Mis,atched closing tag")
                stack.pop()
            elif token["type"] == "name":
                raise Exception("Mismatched closing tag")
                stack.pop()
            elif token["type"] == "text":
                if stack:
                    stack[-1].children.append(SSMLText(token["value"]))
        if len(stack) != 0:
            raise Exception("Unclosed tag")
        
        root = tokens[0]
        if root["name"] != "speak":
            raise Exception("Root must be <speak>")
        
        return build_tree(tokens)
    # raise NotImplementedError()


def ssmlNodeToText(node: SSMLNode) -> str:
    # TODO: implement this function
    raise NotImplementedError()


def unescapeXMLChars(text: str) -> str:
    return text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def escapeXMLChars(text: str) -> str:
    return text.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

# Example usage:
# ssml_string = '<speak>Hello, <break time="500ms"/>world!</speak>'
# parsed_ssml = parseSSML(ssml_string)
# text = ssmlNodeToText(parsed_ssml)
# print(text)