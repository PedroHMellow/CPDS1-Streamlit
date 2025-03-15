from pathlib import Path
import streamlit as st  
from PIL import Image
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, poisson


# Configurações do caminho:
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "Styles" / "main.css"
resume_file = current_dir / "Assets" / "Currículo_temporário.pdf"
profile_pic = current_dir / "Assets" / "Profile picture.png"

# Variáveis
TPagina = "CPDS | PedroHMello"
Nome = "PedroHMello"
Descricao = """
Olá, meu nome é Pedro Henrique Mello, sou estudante de Engenharia de Software na FIAP, com previsão de conclusão em Julho de 2027. Tenho paixão por tecnologia, desenvolvimento de software e resolução de problemas por meio da programação. Ao longo da minha trajetória acadêmica, participei de desafios como o Challenge Hospital HC e o Challenge Rede Âncora, onde pude aplicar meus conhecimentos na prática e desenvolver habilidades essenciais para o mercado de trabalho.

Atualmente, estou buscando uma oportunidade de estágio para aprimorar minhas habilidades e ganhar experiência profissional. Tenho conhecimentos em Python, HTML, CSS, React e Tailwind, além de familiaridade com ferramentas de design como Photoshop. Sou um profissional curioso, dedicado e sempre disposto a aprender novas tecnologias e metodologias.

Acredito que minha capacidade de aprendizado rápido, minha paixão pelo desenvolvimento de software e minhas soft skills em storytelling podem agregar valor a qualquer equipe. Estou ansioso para fazer parte de um ambiente inovador onde possa crescer e contribuir ativamente para projetos desafiadores.
"""
Email = "israelalvesmello2003@gmail.com" 
RedesS = {
    "🔗Linkedin": "https://www.linkedin.com/in/pedro-henrique-mello-80672a252/",
    "🔗Github": "https://github.com/PedroHMellow"
}

# Nav
st.set_page_config(page_title=TPagina)
menu = st.sidebar.radio("Navegação", ["Home", "Skills", "Análise de Dados"])

# Home
if menu == "Home":
    with open(css_file) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
        with open(resume_file, "rb") as pdf_file:
            PDFbyte = pdf_file.read()
        profile_pic = Image.open(profile_pic)

        col1, col2 = st.columns(2, gap="small")
        with col1:
            st.image(profile_pic, width=230)
        
        with col2:
            st.title(Nome)
            st.download_button(
                label="📄 Baixar currículo",
                data=PDFbyte,
                file_name=resume_file.name,
                mime="application/octet-stream",
            )
            st.write("📫", Email)
            cols = st.columns(len(RedesS))
            for index, (platform, link) in enumerate(RedesS.items()):
                cols[index].write(f"[{platform}]({link})")
        
        st.write("###")
        st.subheader("Introdução Pessoal e Objetivo Profissional:")
        st.write(Descricao)
        st.write("###")
        st.subheader("Formação:")
        st.write("""
        - 🎓 FIAP | Engenharia de Software (Previsão de conclusão: Julho de 2027)
        """)
        st.subheader("Experiência:")
        st.write("""
        - 👨🏻‍💻 Programador | Front End para Hospital HC
            -   Revitalização do site do Hospital, com foco na experiência do usuário(UX).
            -   Garantia de acessibilidade para públicos de diferentes faixas etárias.
            -   Priorização da empatia no design, considerando o público infantil.
            -   Utilização de HTML, Tailwind e JavaScript para uma interface intuitiva e responsiva.
        """)
        st.write("---")
        st.write("""
        - 👨🏻‍💻 Programador para Rede Ancora
            -   Projeto em andamento com foco na fidelização de clientes da Rede Âncora.
            -   Desenvolvimento de um website para compra de peças com ambiente 3D interativo.
            -   O ambiente 3D auxilia na modelagem, criação e manutenção de carros.
            -   Tecnologias utilizadas: Maya, Java, HTML, CSS e Python.
        """)

# Skills
elif menu == "Skills":
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        st.subheader("Skills")
        st.write("""
        - ⭐ Linguagens de Programação: Python, HTML, CSS, React e Tailwind 
        - ⭐ Soft Skills: Storytelling
        - ⭐ Extras: Photoshop 
        """)

        categories = ["Linguagens de Programação", "Soft Skills", "Extra"]
        valores = [8, 7, 6]

        df = pd.DataFrame(dict(
            r=valores,
            theta=categories
        ))

        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_traces(fill='toself', line=dict(color='red'))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False
        )
        st.plotly_chart(fig)

# Análise de Dados
elif menu == "Análise de Dados":
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        @st.cache_data
        def load_data():
            file_path = "economic-survey-of-manufacturing-december-2024-quarter.xlsx"
            try:
                xls = pd.ExcelFile(file_path)
                df = pd.read_excel(xls, sheet_name="Table 1", skiprows=9)
                df = df.rename(columns={
                    "SFZ1CA": "Sales (Unadjusted)",
                    "SFZ1CS": "Sales (Seasonally Adjusted)",
                    "SFZ1CT": "Sales (Trend)",
                    "SFZ4CA": "Raw Materials",
                    "SFZ5CA": "Closing Stocks",
                    "SFZ1KA": "Sales Volume",
                    "SFZ1KS": "Sales Volume (Seasonally Adjusted)",
                    "SFZ1KT": "Sales Volume (Trend)",
                    "SFZ5KA": "Closing Stocks Volume"
                })
                df = df.dropna(how='all')  # Remover linhas completamente vazias
                df = df.dropna(axis=1, how='all')  # Remover colunas completamente vazias
                return df
            except Exception as e:
                st.error(f"Erro ao carregar os dados: {e}")
                return pd.DataFrame()

        df = load_data()

        st.header("Análise de Dados - Economic Survey of Manufacturing")
        st.write("Os dados utilizados nesta análise foram extraídos do Economic Survey of Manufacturing - December 2024 Quarter, um relatório econômico sobre a indústria manufatureira. O conjunto de dados contém informações sobre métricas financeiras e operacionais, incluindo dados de vendas, estoques entre outros.")

        # st.header("2)Medidas centrais")


        if df.empty:
            st.warning("Os dados não foram carregados corretamente. Verifique o arquivo e tente novamente.")
        else:
            # Medidas Centrais
            st.header("Medidas Centrais")
            summary_stats = df.describe().T
            st.write(summary_stats[['mean', '50%', 'std', 'min', 'max']].rename(columns={'50%': 'median'}))

            # Analise 
            st.write("Com base nos resultados podemos conluir que:")
            st.write("""
            - A média das vendas ajustadas sazonalmente foi um bom indicador do comportamento geral dos dados.
            -  A mediana mostrou que a distribuição dos dados não era extremamente assimétrica, já que ficou próxima da média.
            - A moda não foi relevante em algumas variáveis porque os dados eram contínuos e não tinham valores repetidos suficientes para determinar um valor predominante.
            """)
        

            st.write("---")

            # Análise da distribuição
            st.header("Distribuição dos Dados")
            selected_variable = st.selectbox("Escolha uma variável para visualizar:", df.columns)

            fig, ax = plt.subplots(figsize=(8, 5))  
            sns.histplot(df[selected_variable].dropna(), bins=15, kde=True, ax=ax)
            ax.set_title(f"Distribuição de {selected_variable}")
            ax.set_xlabel(selected_variable)
            ax.set_ylabel("Frequência")
            plt.xticks(rotation=45)  
            st.pyplot(fig)

            # Analise 
            st.write("Conclusão: Os dados principais analisados, especialmente as vendas ajustadas, seguem um comportamento relativamente previsível, com pouca assimetria, o que permite aplicar modelos estatísticos como a distribuição normal para previsões futuras. Entretanto, algumas variáveis podem precisar de transformações ou modelos mais específicos devido à dispersão elevada.")

            st.write("---")

        
        # st.header("3)Aplicação")

        # Distribuição Normal
        st.subheader("Distribuição Normal")
        
        sales_data = df["Sales (Seasonally Adjusted)"].dropna()
        mu, sigma = sales_data.mean(), sales_data.std()
        x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
        y = norm.pdf(x, mu, sigma)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(sales_data, bins=15, kde=True, stat="density", ax=ax)
        ax.plot(x, y, 'r-', label="Distribuição Normal")
        ax.set_title("Distribuição Normal das Vendas Ajustadas Sazonalmente")
        ax.set_xlabel("Vendas")
        ax.set_ylabel("Densidade")
        ax.legend()
        st.pyplot(fig)

        # Analise
        st.write("Com base nos resultados podemos conluir que:")
        st.write("""
        - Média e Simetria: Os valores das vendas ajustadas sazonalmente ficaram concentrados ao redor da média, o que indica um comportamento previsível e estável.
        -  Comparação com a Curva Normal: Quando sobrepomos a curva da distribuição normal ao histograma dos dados, observamos que ela se ajusta bem ao formato dos dados, reforçando a hipótese de normalidade.
        - Desvio Padrão: O desvio padrão mostrou que a maioria dos valores está dentro de um intervalo previsível ao redor da média, sem grandes variações extremas.
        """)

        st.write("---")


        # Distribuição de Poisson
        st.subheader("Distribuição de Poisson")
        st.write("A distribuição de Poisson é aplicada para modelar a ocorrência de eventos em um intervalo de tempo fixo.")
        
        lambda_poisson = sales_data.mean() / 1000  # Normalizando para valores razoáveis
        x_poisson = np.arange(0, max(sales_data)//1000)
        y_poisson = poisson.pmf(x_poisson, lambda_poisson)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(x_poisson, y_poisson, color='purple', alpha=0.6, label="Distribuição de Poisson")
        ax.set_title("Distribuição de Poisson - Modelagem de Eventos")
        ax.set_xlabel("Ocorrências por unidade")
        ax.set_ylabel("Probabilidade")
        ax.legend()
        st.pyplot(fig)

        # Analise
        st.write("Os dados indicam que a maior parte dos períodos apresenta vendas dentro de um certo padrão, mas há alguns momentos com ocorrências acima do esperado. Isso pode ser útil para prever sazonalidades e preparar estratégias para períodos de alta demanda.")
