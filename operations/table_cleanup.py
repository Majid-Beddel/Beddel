# operations/table_cleanup.py

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def process(doc, **kwargs):
    for table in doc.tables:
        num_cols = len(table.columns)
        even_width = 10000 // num_cols if num_cols else 2500  # Fallback width

        for row in table.rows:
            tr = row._tr
            trPr = tr.get_or_add_trPr()

            # Set fixed height
            trHeight = OxmlElement('w:trHeight')
            trHeight.set(qn('w:val'), '500')
            trHeight.set(qn('w:hRule'), 'exact')
            trPr.append(trHeight)

            for cell in row.cells:
                # Normalize alignment
                for para in cell.paragraphs:
                    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    # Strip extra whitespace
                    para.text = para.text.strip()

                # Normalize cell width
                tc_pr = cell._tc.get_or_add_tcPr()
                tc_w = OxmlElement('w:tcW')
                tc_w.set(qn('w:type'), 'dxa')
                tc_w.set(qn('w:w'), str(even_width))
                tc_pr.append(tc_w)

                # Remove broken vertical merges
                v_merge = tc_pr.find(qn('w:vMerge'))
                if v_merge is not None:
                    tc_pr.remove(v_merge)