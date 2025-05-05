# Monitoramento de Obras Públicas - PROJETO EM ANDAMENTO


> Esse é um projeto pessoal voltado para fins de aprendizado.

Está é uma plataforma que identifica atrasos, desvios orçamentários e riscos, utilizando o Neo4j para análise integrada e o Playwright para extração de dados do painel [Obrasgov.br](https://dd-publico.serpro.gov.br/extensions/cipi/cipi.html) da Rede Parcerias.

## Tecnologias Utilizadas

- **Python**: 3.12.0 (pre-requisito)
- **Neo4j**: ???????5.12.0 (pre-requisito)
- **Playwright**: 1.47.0


## Como Executar

1. **Baixe o projeto**:
2. **Execute o script de configuaração no CMD**:
     ```bash
     setup.bat
    ```
    Isso cria um ambiente virtual, instala dependências (Playwright, Pandas, etc.) e baixa os navegadores do Playwright.

3. **Ativar o ambiente virtual**
    ```bash
     .\venv\Scripts\activate
    ```

4. **Execute a extração dos dados**
    ```bash
     python3 extract.py
    ```