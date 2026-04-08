import sys
import subprocess
import os

# Garantia de instalação da biblioteca necessária
try:
    from fpdf import FPDF
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf2"])
    from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Header só aparece da página 2 em diante para manter a capa limpa
        if self.page_no() > 1:
            self.set_font("helvetica", "B", 8)
            self.set_text_color(180, 180, 180)
            self.cell(0, 10, "GamerVault Pro | Technical Integration Handbook", align="R")
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"GamerVault Pro | Page {self.page_no()}", align="C")

def create_pdf():
    pdf = PDF()
    
    # --- PÁGINA 1: CAPA (BANNER FOCO PC) ---
    pdf.add_page()
    banner_path = r"C:\Users\SCVic\.gemini\antigravity\brain\d8d94e67-be87-4b3e-9f98-56773d155a4d\pc_gamervault_pro_banner_1775586500619.png"
    if os.path.exists(banner_path):
        # Banner posicionado para impacto visual máximo na primeira página
        pdf.image(banner_path, x=10, y=85, w=190)
    
    # --- PÁGINA 2: CONTEÚDO ESTRATÉGICO E SEO ---
    pdf.add_page()
    pdf.set_y(25)
    
    # Título Principal
    pdf.set_font("helvetica", "B", 24)
    pdf.set_text_color(10, 20, 50) # Navy Blue
    pdf.cell(0, 12, "TECHNICAL REPORT", new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "High-Precision PC Gaming Deals & Regional Price Integration", new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.ln(10)

    # Conteúdo Técnico com SEO Oculto
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "1. Real-Time Ingestion: Steam & Epic Ecosystem", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 7, "GamerVault Pro utilizes a multi-threaded scraping architecture specifically optimized for the PC ecosystem. This ensures our daily PC gaming deals are delivered with sub-second latency. By monitoring the Steam price tracker API endpoints and direct Epic Games storefronts, we eliminate the 24-hour delay common in other aggregators.")
    pdf.ln(5)

    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "2. Regional Pricing Reliability (TRY/ARS)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 11)
    pdf.multi_cell(0, 7, "Our unique selling proposition lies in the accuracy of our Steam regional pricing data. Unlike apps that rely on estimated conversion math, GamerVault Pro fetches native prices directly from the Turkey (TRY) and Argentina (ARS) stores. This level of detail is critical for builders of cheap Steam games trackers and regional price arbitrage tools.")
    pdf.ln(5)

    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "3. Proprietary Live FX Conversion Engine", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 11)
    pdf.multi_cell(0, 7, "Designed for the ULTRA tier, our Live FX Engine offers real-time currency conversion for games. All regional prices can be transformed into USD, EUR, or BRL using a synchronized 6-hour FX cache. This hybrid approach provides developers with the stability of a cached system and the precision of live market tracking.")
    pdf.ln(5)

    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "4. Enterprise Security Handshake", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 11)
    pdf.multi_cell(0, 7, "Security is managed through the RapidAPI Proxy Secret handshake, ensuring high data integrity. This protocol prevents unauthorized backend access and provides a robust firewall against SQL and JS injection, making GamerVault Pro a production-ready solution for high-traffic gaming dashboards.")
    pdf.ln(15)
    
    # Rodapé de Autoridade
    pdf.set_font("helvetica", "I", 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, "Verified high-precision resource for PC Gaming developers.", align="C")

    output_path = r"c:\Users\SCVic\OneDrive\Documentos\API\gamer_vault_pro\gamervault_pro_technical_handbook.pdf"
    pdf.output(output_path)
    print(f"PDF gerado em: {output_path}")

if __name__ == "__main__":
    create_pdf()
