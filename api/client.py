import requests
import os


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def update_endpoint(self, new_base_url):
        self.base_url = new_base_url.rstrip('/')

    def parse_pdf(self, pdf_path, bom_path=None, manager_path=None, bom_sheet_index=0):
        url = f"{self.base_url}/api/parse-pdf"

        files = {
            'pdf_file': ('document.pdf', open(pdf_path, 'rb'), 'application/pdf')
        }

        if bom_path and os.path.exists(bom_path):
            files['excel_bom'] = ('bom.xlsx', open(bom_path, 'rb'),
                                  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        if manager_path and os.path.exists(manager_path):
            files['excel_manager'] = ('manager.xlsx', open(manager_path, 'rb'),
                                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        data = {'bom_sheet_index': bom_sheet_index}

        try:
            response = requests.post(url, files=files, data=data, timeout=120)

            for file_obj in files.values():
                if hasattr(file_obj[1], 'close'):
                    file_obj[1].close()

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"API Error: {str(e)}"
            }

    def export_excel(self, api_response, output_path):
        url = f"{self.base_url}/api/export-excel"

        try:
            response = requests.post(url, json=api_response, timeout=60, stream=True)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ Export error: {e}")
            return False
