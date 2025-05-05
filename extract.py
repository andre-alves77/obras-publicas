import asyncio
from playwright.async_api import async_playwright
import os

URL = "https://dd-publico.serpro.gov.br/extensions/cipi/cipi.html"
OUTPUT_DIR = os.path.abspath("data")

# id da tabela para o qlikview | nome do arquivo | classe da aba da respectiva tabela no painel 
TABLES = [
    {"id": "qtQdRKF", "name": "Intervencao", "tab": "pills-intervencao-tab"},
    {"id": "MSDA", "name": "Empenho", "tab": "pills-empenho-subtab", "parent_tab": "pills-execucao-financeira-tab"},
    {"id": "GYjmkP", "name": "Pagamentos", "tab": "pills-pagamento-subtab", "parent_tab": "pills-execucao-financeira-tab"},
    {"id": "PzB", "name": "Restos_a_Pagar", "tab": "pills-restos-pagar-subtab", "parent_tab": "pills-execucao-financeira-tab"},
    {"id": "JnAEPV", "name": "Contrato", "tab": "pills-contrato-tab"},
    {"id": "BkkNDzR", "name": "Execucao_Fisica", "tab": "pills-execucao-fisica-tab"},
    {"id": "pjmTbMj", "name": "Emendas", "tab": "pills-emendas-tab"}
]

async def main():
    async with async_playwright() as p:
                
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        print("Abrindo painel...")
        await page.goto(URL)
        await page.wait_for_load_state("networkidle")


        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if "Erro" in msg.text or "error" in msg.text.lower() else None)

        for table in TABLES:
            try:
                
                if "parent_tab" in table:
                    print(f"Ativando aba principal {table['parent_tab']}...")
                    await page.click(f"#{table['parent_tab']}", timeout=10000)
                    await page.wait_for_timeout(5000)

                
                print(f"Ativando aba {table['tab']} para {table['name']}...")
                await page.click(f"#{table['tab']}", timeout=10000)
                await page.wait_for_timeout(5000)

                
                print(f"Exportando {table['name']}...")
                async with page.expect_download(timeout=60000) as download_info:
                    await page.evaluate("""
                        require(["js/qlik"], function(qlik) {
                            return new Promise((resolve) => {
                                app.getObject('%s').then(function(model) {
                                    var table = qlik.table(model);
                                    table.exportData({ download: true });
                                    setTimeout(resolve, 3000);
                                }).catch(function(error) {
                                    console.error('Erro ao exportar %s:', error);
                                    resolve();
                                });
                            });
                        });
                    """ % (table["id"], table["name"]))
                    download = await download_info.value
                    await download.save_as(os.path.join(OUTPUT_DIR, f"{table['name']}.xlsx"))
                    print(f"Arquivo salvo: {table['name']}.xlsx")
            except Exception as e:
                print(f"Falha ao exportar {table['name']}: {e}")

        if errors:
            print("Erros detectados no console:")
            for error in errors:
                print(f"- {error}")

        await browser.close()
        print("Concluído!")

if __name__ == "__main__":
    asyncio.run(main())