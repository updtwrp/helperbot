import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
from datetime import datetime

class XMLViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("XML Editor")
        self.geometry("600x400")

        self.text = tk.Text(self, wrap=tk.NONE)
        self.text.pack(fill=tk.BOTH, expand=1)

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.load_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)

    def new_file(self):
        template = '''<documents version="1.36">
    <withdrawal action_id="552">
        <subject_id></subject_id>
        <operation_date>{operation_date}</operation_date>
        <doc_num></doc_num>
        <doc_date>{doc_date}</doc_date>
        <withdrawal_type>13</withdrawal_type>
        <order_details></order_details>
    </withdrawal>
</documents>'''
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + "+03:00"
        doc_date = datetime.now().strftime('%d.%m.%Y')
        formatted_template = template.format(operation_date=current_time, doc_date=doc_date)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, formatted_template)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    xml_content = file.read()
                    loaded_xml = ET.fromstring(xml_content)

                    subject_id = loaded_xml.find('.//subject_id').text if loaded_xml.find('.//subject_id') is not None else ""
                    doc_num = loaded_xml.find('.//doc_num').text if loaded_xml.find('.//doc_num') is not None else ""
                    sgtin_elements = loaded_xml.findall('.//sgtin')
                    sscc_elements = loaded_xml.findall('.//sscc')
                    sgtin_lines = "\n".join([f"            <sgtin>{sgtin.text}</sgtin>" for sgtin in sgtin_elements])
                    sscc_lines = "\n".join([f"            <sscc>{sscc.text}</sscc>" for sscc in sscc_elements])

                    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + "+03:00"
                    doc_date = datetime.now().strftime('%d.%m.%Y')

                    template = f'''<documents version="1.36">
    <withdrawal action_id="552">
        <subject_id>{subject_id}</subject_id>
        <operation_date>{current_time}</operation_date>
        <doc_num>{doc_num}</doc_num>
        <doc_date>{doc_date}</doc_date>
        <withdrawal_type>13</withdrawal_type>
        <order_details>{sgtin_lines}
{sscc_lines}
        </order_details>
    </withdrawal>
</documents>'''
                    self.text.delete(1.0, tk.END)
                    self.text.insert(tk.END, template)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file: {e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml"), ("All files", "*.*")])
        if file_path:
            try:
                xml_content = self.text.get(1.0, tk.END).strip()
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(xml_content)
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

if __name__ == "__main__":
    app = XMLViewer()
    app.mainloop()
