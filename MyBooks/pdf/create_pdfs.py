import os
import markdown
import pdfkit
import sys

# Configuração do caminho para o wkhtmltopdf
# Nota: Você precisa ter o wkhtmltopdf instalado no seu sistema
# Download: https://wkhtmltopdf.org/downloads.html
# wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
# config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

def markdown_to_pdf(markdown_file, pdf_file):
    """Converte um arquivo Markdown para PDF."""
    # Ler o conteúdo do arquivo Markdown
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Converter Markdown para HTML
    html_content = markdown.markdown(markdown_content, extensions=['tables'])
    
    # Adicionar estilos CSS para melhorar a aparência
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 40px;
            }}
            h1, h2, h3 {{
                color: #333;
            }}
            h1 {{
                border-bottom: 2px solid #333;
                padding-bottom: 10px;
            }}
            h2 {{
                border-bottom: 1px solid #ccc;
                padding-bottom: 5px;
                margin-top: 30px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
                text-align: left;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            code {{
                background-color: #f5f5f5;
                padding: 2px 5px;
                border-radius: 3px;
                font-family: Consolas, monospace;
            }}
            pre {{
                background-color: #f5f5f5;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Salvar o HTML temporariamente
    html_file = pdf_file.replace('.pdf', '.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(styled_html)
    
    # Converter HTML para PDF
    try:
        # Se você tiver o wkhtmltopdf configurado:
        # pdfkit.from_file(html_file, pdf_file, configuration=config)
        
        # Sem configuração específica:
        pdfkit.from_file(html_file, pdf_file)
        print(f"PDF criado com sucesso: {pdf_file}")
    except Exception as e:
        print(f"Erro ao criar PDF: {e}")
        # Alternativa: manter o HTML como saída
        print(f"HTML criado como alternativa: {html_file}")
        return False
    
    # Remover o arquivo HTML temporário
    # os.remove(html_file)
    return True

def main():
    """Função principal para converter os arquivos Markdown para PDF."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(base_dir, 'docs')
    pdf_dir = os.path.join(base_dir, 'pdf')
    
    # Garantir que o diretório PDF existe
    os.makedirs(pdf_dir, exist_ok=True)
    
    # Arquivos a serem convertidos
    files_to_convert = [
        ('user_stories.md', 'User_Stories.pdf'),
        ('diagramas.md', 'Diagramas.pdf'),
        ('planejamento_iteracoes.md', 'Planejamento_Iteracoes.pdf')
    ]
    
    for md_file, pdf_file in files_to_convert:
        md_path = os.path.join(docs_dir, md_file)
        pdf_path = os.path.join(pdf_dir, pdf_file)
        
        if os.path.exists(md_path):
            print(f"Convertendo {md_file} para PDF...")
            success = markdown_to_pdf(md_path, pdf_path)
            if not success:
                print(f"Falha ao converter {md_file}. Verifique se o wkhtmltopdf está instalado.")
        else:
            print(f"Arquivo não encontrado: {md_path}")

if __name__ == "__main__":
    main()
