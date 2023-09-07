from lxml import etree


MY_NAMESPACES = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main',
}


def set_slide_duration(slide, duration):
    """Sets the duration of a slide by creating and inserting XML elements.

    Parameters
    ----------
    slide : pptx.slide.Slide
        The slide for which to set the duration.
    duration : float
        The duration to set for the slide, in seconds.

    Returns
    -------
    None
    """
    milli_duration = int(duration * 1000.0)
    slide_tree = slide._element

    alt_cnt_xml = slide_tree.find('{%s}AlternateContent' % MY_NAMESPACES['mc'])
    insert = False
    if alt_cnt_xml is None:
        insert = True
        alt_cnt_xml = etree.Element(
            '{%s}AlternateContent' % MY_NAMESPACES['mc'], nsmap=MY_NAMESPACES)

    choice_xml = alt_cnt_xml.find('{%s}Choice' % MY_NAMESPACES['mc'])
    if choice_xml is None:
        choice_xml = etree.SubElement(
            alt_cnt_xml, '{%s}Choice' % MY_NAMESPACES['mc'],
            nsmap=MY_NAMESPACES)

    choice_xml.set("Requires", "p14")
    transition_xml = choice_xml.find('{%s}transition' % MY_NAMESPACES['p'])
    if transition_xml is None:
        transition_xml = etree.SubElement(
            choice_xml, '{%s}transition' % MY_NAMESPACES['p'],
            nsmap=MY_NAMESPACES)
    transition_xml.set("spd", "slow")
    transition_xml.set("{%s}dur" % MY_NAMESPACES['p14'], "2000")
    transition_xml.set("advClick", "0")
    transition_xml.set("advTm", str(milli_duration))

    fallback_xml = alt_cnt_xml.find('{%s}Fallback' % MY_NAMESPACES['mc'])
    if fallback_xml is None:
        fallback_xml = etree.SubElement(
            alt_cnt_xml, '{%s}Fallback' % MY_NAMESPACES['mc'],
            nsmap=MY_NAMESPACES)
    transition_f_xml = alt_cnt_xml.find('{%s}transition' % MY_NAMESPACES['p'])
    if transition_f_xml is None:
        transition_f_xml = etree.SubElement(
            fallback_xml, '{%s}transition' % MY_NAMESPACES['p'],
            nsmap=MY_NAMESPACES)
    transition_f_xml.set("spd", "slow")
    transition_f_xml.set("advClick", "0")
    transition_f_xml.set("advTm", str(milli_duration))
    if insert:
        slide_tree.insert(2, alt_cnt_xml)  # has to go before timing block


def delete_slide_transition(slide):
    slide_tree = slide._element

    alt_cnt_xml = slide_tree.find('{%s}AlternateContent' % MY_NAMESPACES['mc'])
    insert = False
    if alt_cnt_xml is None:
        insert = True
        alt_cnt_xml = etree.Element(
            '{%s}AlternateContent' % MY_NAMESPACES['mc'], nsmap=MY_NAMESPACES)

    choice_xml = alt_cnt_xml.find('{%s}Choice' % MY_NAMESPACES['mc'])
    if choice_xml is None:
        choice_xml = etree.SubElement(
            alt_cnt_xml, '{%s}Choice' % MY_NAMESPACES['mc'],
            nsmap=MY_NAMESPACES)

    choice_xml.set("Requires", "p14")
    transition_xml = choice_xml.find('{%s}transition' % MY_NAMESPACES['p'])
    if transition_xml is None:
        transition_xml = etree.SubElement(
            choice_xml, '{%s}transition' % MY_NAMESPACES['p'],
            nsmap=MY_NAMESPACES)
    transition_xml.set("advClick", "1")
    transition_xml.attrib.pop("advTm", None)

    fallback_xml = alt_cnt_xml.find('{%s}Fallback' % MY_NAMESPACES['mc'])
    if fallback_xml is None:
        fallback_xml = etree.SubElement(
            alt_cnt_xml, '{%s}Fallback' % MY_NAMESPACES['mc'],
            nsmap=MY_NAMESPACES)
    transition_f_xml = alt_cnt_xml.find('{%s}transition' % MY_NAMESPACES['p'])
    if transition_f_xml is None:
        transition_f_xml = etree.SubElement(
            fallback_xml, '{%s}transition' % MY_NAMESPACES['p'],
            nsmap=MY_NAMESPACES)
    transition_f_xml.set("advClick", "1")
    transition_f_xml.attrib.pop("advTm",  None)
    if insert:
        slide_tree.insert(2, alt_cnt_xml)  # has to go before timing block
