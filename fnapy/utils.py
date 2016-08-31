#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

"""
Useful functions
"""

from bs4 import BeautifulSoup
from lxml import etree
from config import *
import re
import xmltodict
import itertools


# CLASSES

# TODO Implement a check for the attributes
class Message(object):
    ACTIONS = (
        'mark_as_read', 'mark_as_unread', 'archive',
        'mark_as_read_and_archive', 'unarchive', 'reply', 'create'
    )

    TO = (
        'CALLCENTER', 'CLIENT', 'ALL'
    )

    SUBJECTS = (
        'product_information', 'shipping_information', 'order_information', 
        'offer_problem', 'offer_not_received', 'other_question'
    )

    TYPES = ('ORDER', 'OFFER')

    def __init__(self, action, id, to='ALL', description='', subject='', type='ORDER'): 
        self._action = action
        self._id = id
        self._to = to
        self._description = description
        self._subject = subject
        self._type = type

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, new_value):
        if new_value not in Message.ACTIONS:
            msg = 'Invalid action. Choose between {}.'.format(Message.ACTIONS)
            raise ValueError(msg)
        self._action = new_value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_value):
        self._id = new_value

    @property
    def to(self):
        return self._to

    @to.setter
    def to(self, new_value):
        if new_value not in Message.TO:
            msg = 'Invalid recipient. Choose between {}.'.format(Message.TO)
            raise ValueError(msg)
        self._to = new_value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_value):
        self._description = new_value

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, new_value):
        if new_value not in Message.SUBJECTS:
            msg = 'Invalid subject. Choose between {}'.format(Message.SUBJECTS)
            raise ValueError(msg)
        self._subject = new_value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_value):
        if new_value not in Message.TYPES:
            msg = 'Invalid type. Choose between {}'.format(Message.TYPES)
            raise ValueError(msg)
        self._type = new_value

    def __repr__(self):
        r = '<Message: action={self.action}, id={self.id}, to={self.to}, '
        r += 'description={self.description}, subject={self.subject}, '
        r += 'type={self.type}>'
        return r.format(self=self)

    def __str__(self):
        return """Message
action     : {self.action}
id         : {self.id}
to         : {self.to}
description: {self.description}
subject    : {self.subject}
type       : {self.type}
        """.format(self=self)

    def to_dict(self):
        """Return the a dictionary in the xmltodict format"""
        message = {'message': {
            '@action': self.action,
            '@id': self.id,
            'message_to': {'#text': self.to},
            'message_subject': {'#text': self.subject},
            'message_description': {'#text': self.description},
            'message_type': {'#text': self.type},
        }}
        return message



# FUNCTIONS
def extract_text_from_tag(root, name):
    """Returns the text in the tag name

    If the tag is not found and empty string is returned
    """
    tag = root.find(name)
    if tag:
        text = tag.text
    else:
        text = u''
    return text


def dict2xml(_dict):
    """Returns a XML string from the input dictionary"""
    xml = xmltodict.unparse(_dict, pretty=True)
    xmlepured = remove_namespace(xml)
    return xmlepured


def remove_namespace(xml):
    """Remove the namespace from the XML string"""
    xmlepured = re.sub(pattern=' xmlns="[^"]+"', repl='', string=xml, flags=0)
    xmlepured = xmlepured.encode('utf-8')
    return xmlepured

# TODO Use process_namespaces
def xml2dict(xml):
    """Returns a dictionary from the input XML
    
    :type xml: unicode
    :param xml: The XML

    :rtype: dict
    :returns: the dictionary correspoding to the input XML
    """
    xmlepured = remove_namespace(xml)
    return xmltodict.parse(xmlepured)


# TODO Parse the token with lxml instead of BeautifulSoup
def parse_xml(response, tag_name):
    """Get the text contained in the tag of the response

    :param response: the Response
    :param tag_name: the name of the tag
    :returns: the text enclosed in the tag
    
    """
    return BeautifulSoup(response.content, 'lxml').find(tag_name).text


def parse_offer(offer_tag):
    """Parse the XML returned by the offer tag
    
    :type offer_tag: bs4.element.Tag
    :param offer_tag: The offer tag generated

    :rtype: FnacOffer
    :returns: the corresponding FnacOffer instance
    """
    fnac_offer = FnacOffer()
    for attr in fnac_offer.__dict__:
        setattr(fnac_offer, attr, extract_text_from_tag(offer_tag, attr))
    return fnac_offer


# TODO Refactor to read the attributes from the object
def parse_offers_query_response(response):
    """Parse the response sent by offers_query

    :type response: requests.Response
    :param response: the response sent by the offers_query request

    :rtype: FnacOffersQueryResponse
    :returns: response
    """
    offers_query_response = FnacOffersQueryResponse()
    soup = BeautifulSoup(response.content, 'lxml')
    offers_query_response.page = soup.find('page').text
    offers_query_response.total_paging = soup.find('total_paging').text
    offers_query_response.nb_total_per_page = soup.find('nb_total_per_page').text
    offers_query_response.nb_total_result = soup.find('nb_total_result').text

    offer_tags = soup.find_all('offer')
    for offer_tag in offer_tags:
        offers_query_response.offers.append(parse_offer(offer_tag))

    offers_query_response.response = response
    return offers_query_response
    

def create_offer_element(product_reference, offer_reference, price, product_state, quantity, description=None):
    """Create an offer element

    An offer needs 5 mandatory parameters:
    :param product_reference: a product reference (such as EAN)
    :param offer_reference: a seller offer reference (such as SKU)
    :param product_state: a product state
    :param price: a price
    :param quantity: a quantity

    You may add an optional parameter:
    :param description: a description of the product

    :returns: offer (etree.Element)

    """
    offer = etree.Element('offer')
    etree.SubElement(offer, "product_reference" ,type="Ean").text = str(product_reference)
    etree.SubElement(offer, "offer_reference", type="SellerSku").text = etree.CDATA(offer_reference)
    etree.SubElement(offer, "price").text = str(price)
    etree.SubElement(offer, "product_state").text = str(product_state)
    etree.SubElement(offer, "quantity").text = str(quantity)
    if description:
        etree.SubElement(offer, "description").text = etree.CDATA(description)
    return offer


def create_xml_element(connection, token, name):
    """A helper function creating an etree.Element with the necessary
    attributes

    :param name: The name of the element
    :returns: etree.Element

    """
    return etree.Element(name, nsmap={None: XHTML_NAMESPACE},
            shop_id=connection.shop_id, partner_id=connection.partner_id, token=token)


def get_order_ids(orders_query_response):
    """Returns the order_ids in orders_query_response"""
    orders = orders_query_response['orders_query_response'].get('order', None)
    order_ids = []
    if orders:
        if isinstance(orders, (list, tuple)):
            for order in orders:
                order_ids.append(order.get('order_id', ''))
        elif isinstance(orders, dict):
            order_ids.append(orders.get('order_id', ''))
    return order_ids


def dmap(fn, collection):
    values = (fn(v) for k, v in record.items())
    return dict(itertools.zip(record, values))

