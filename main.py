import yuag

"""
العنوان:
size: 18
color: 5460819
font: 29LTRiwaya-Bold

الكلام العادي:
size: 16.994998931884766, 18.0
color: 0
font: TimesNRMTPro, TimesNRMTPro-Italic, NotoSansArabic-Bold

الحديث:
size: 16.994998931884766, 18
color: 19116
font: TimesNRMTPro, NotoSansArabic-Bold

مصدر الحديث:
size: 10.994999885559082, 12.997499465942383, 13.994999885559082
color: 5460819, 0
font: TimesNRMTPro-BoldItalic, TimesNRMTPro-Italic
"""

pages_content = []
output_data = {}
for page_num in [10, 13, 14, 15, 30]:
    data = yuag.pdf_page_to_elements("book.pdf", page_num-1)
    yuag.saveJSON(data, "001- blocks.json")

    for block_i, block in enumerate(data): # فقرة
        for line_i, line in enumerate(block["lines"]): # سطر
            for span_i, span in enumerate(line["spans"]): # جزء من سطر
                size = span["size"]
                color = span["color"]
                font = span["font"]

                text: str = span["text"]

                # العنوان
                if size == 18 and color == 5460819 and font == "29LTRiwaya-Bold":
                    if len(pages_content) > 0 and pages_content[-1]["Type"] == "Head":
                        if span_i == 0 and line_i == 0:
                            pages_content[-1]["Text"] += "\n" + text.strip()
                        else:
                            pages_content[-1]["Text"] += " " + text.strip()
                        
                        pages_content[-1]["Text"] = yuag.removeSpaces(pages_content[-1]["Text"], True)
                    else:
                        pages_content.append({"Type": "Head", "Text": yuag.removeSpaces(text, True)})

                # الكلام
                elif size in [16.994998931884766, 18] and color == 0 and font in ["TimesNRMTPro", "TimesNRMTPro-Italic", "NotoSansArabic-Bold"]:
                    if len(pages_content) > 0 and pages_content[-1]["Type"] == "Text":
                        if span_i == 0 and line_i == 0:
                            pages_content[-1]["Text"] += "\n" + text.strip()
                        else:
                            pages_content[-1]["Text"] += " " + text.strip()
                        
                        pages_content[-1]["Text"] = yuag.removeSpaces(pages_content[-1]["Text"], True)
                    else:
                        pages_content.append({"Type": "Text", "Text": yuag.removeSpaces(text, True)})
                                
                # الحديث
                elif size in [16.994998931884766, 18] and color == 19116 and font in ["TimesNRMTPro", "NotoSansArabic-Bold"]:
                    if len(pages_content) > 0 and pages_content[-1]["Type"] == "Hadith":
                        if span_i == 0 and line_i == 0:
                            pages_content[-1]["Text"] += "\n" + text.strip()
                        else:
                            pages_content[-1]["Text"] += " " + text.strip()
                        
                        pages_content[-1]["Text"] = yuag.removeSpaces(pages_content[-1]["Text"], True)
                    else:
                        pages_content.append({"Type": "Hadith", "Text": yuag.removeSpaces(text, True)})
                    
                # مصدر الحديث
                elif size in [10.994999885559082, 12.997499465942383, 13.994999885559082] and color in [5460819, 0] and font in ["TimesNRMTPro-BoldItalic", "TimesNRMTPro-Italic"]:
                    if len(pages_content) > 0 and pages_content[-1]["Type"] == "Hadith resource":
                        if span_i == 0 and line_i == 0:
                            pages_content[-1]["Text"] += "\n" + text.strip()
                        else:
                            if pages_content[-1]["Text"] == "[":
                                pages_content[-1]["Text"] += text.strip()
                            else:
                                pages_content[-1]["Text"] += " " + text.strip()
                        
                        pages_content[-1]["Text"] = yuag.removeSpaces(pages_content[-1]["Text"], True)
                    else:
                        pages_content.append({"Type": "Hadith resource", "Text": yuag.removeSpaces(text, True)})

    active_head = None
    for i, item in enumerate(pages_content):
        if item["Type"] == "Head":
            active_head = item["Text"]
            output_data[active_head] = ""
        else:
            output_data[active_head] += "\n" + item["Text"]
            output_data[active_head] = output_data[active_head].strip()

yuag.saveJSON(output_data, "003- output.json")
yuag.saveJSON(pages_content, "002- content.json")