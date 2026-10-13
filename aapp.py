import streamlit as st

# Configuración de la página (ancho completo y título de la pestaña)
st.set_page_config(
    page_title="Actualidad literaria: una cartografía",
    page_icon="📚",
    layout="wide",
)

# --- BASE DE DATOS DE EJEMPLO (Mock Data) ---
corpus_literario = [
    {
        "nombre": "Canal Letra Muerta",
        "tema": "Reseña de Mariana Enríquez",
        "canal": "YouTube",
        "palabras_clave": ["siniestro", "atmósfera", "realismo mágico", "terror"],
        "opinion": "Positiva",
        "resumen": (
            "Valora la capacidad de la autora para construir climas"
            " terroríficos anclados en el conurbano."
        ),
        "link": "https://youtube.com",
    },
    {
        "nombre": "Revista Otra Parte",
        "tema": "Ensayo sobre Fogwill y los 80",
        "canal": "Revista Cultural",
        "palabras_clave": [
            "dictadura",
            "ficción",
            "humor negro",
            "canon argentino",
        ],
        "opinion": "Positiva",
        "resumen": (
            "Analiza la vigencia de la novela Los pichiciegos para pensar la"
            " memoria histórica desde la ironía."
        ),
        "link": "https://revistaotraparte.com",
    },
    {
        "nombre": "@lector_critico_x",
        "tema": "Debate sobre Ulises de James Joyce",
        "canal": "X (Twitter)",
        "palabras_clave": ["pretencioso", "ilegible", "clásico", "modernismo"],
        "opinion": "Negativa",
        "resumen": (
            "Argumenta que es un libro inaccesible y poco disfrutable para la"
            " lectura cotidiana contemporánea."
        ),
        "link": "https://twitter.com",
    },
    {
        "nombre": "BookTok Argentina",
        "tema": "Recomendación de Samanta Schweblin",
        "canal": "TikTok",
        "palabras_clave": ["distopía", "inquietante", "terror", "atmósfera"],
        "opinion": "Positiva",
        "resumen": (
            "Destaca el formato de cuento largo y cómo genera suspenso extremo"
            " en pocas páginas."
        ),
        "link": "https://tiktok.com",
    },
    {
        "nombre": "Fósforo Podcast",
        "tema": "Entrevista a poetas contemporáneos",
        "canal": "YouTube",
        "palabras_clave": ["poesía", "voz", "orillero", "canon argentino"],
        "opinion": "Neutra",
        "resumen": (
            "Debate sobre las nuevas editoriales independientes y la"
            " circulación de la poesía joven."
        ),
        "link": "https://youtube.com",
    },
]

# --- SECCIÓN 1: BANNER DE PRESENTACIÓN ---
st.title("📚 Actualidad literaria: una cartografía")
st.markdown(
    "*Una herramienta interactiva para explorar la circulación, recepción y"
    " discusión del campo literario en plataformas digitales y revistas"
    " culturales.*"
)
st.markdown("---")

# --- SECCIÓN 2: BUSCADOR Y FILTROS ---
st.subheader("🔍 Explorar el corpus")

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    canales_disponibles = ["Todos"] + list(
        set([item["canal"] for item in corpus_literario])
    )
    filtro_canal = st.selectbox("Canal / Plataforma", canales_disponibles)

with col_f2:
    temas_disponibles = ["Todos"] + list(
        set([item["tema"] for item in corpus_literario])
    )
    filtro_tema = st.selectbox("Temática / Autor", temas_disponibles)

with col_f3:
    busqueda_texto = st.text_input(
        "Palabras clave (ej: terror, canon, atmósfera)"
    )

with st.expander("⚙️ Filtro avanzado (Sentimiento / Opinión)"):
    filtro_opinion = st.selectbox(
        "Opinión del contenido", ["Todas", "Positiva", "Negativa", "Neutra"]
    )

# --- LÓGICA DE FILTRADO ---
resultados_filtrados = []
for item in corpus_literario:
    if filtro_canal != "Todos" and item["canal"] != filtro_canal:
        continue
    if filtro_tema != "Todos" and item["tema"] != filtro_tema:
        continue
    if (
        filtro_opinion != "Todas"
        and item["opinion"].lower() != filtro_opinion.lower()
    ):
        continue
    if busqueda_texto:
        texto_busqueda = busqueda_texto.lower()
        coincide_palabra = any(
            texto_busqueda in p.lower() for p in item["palabras_clave"]
        )
        coincide_resumen = texto_busqueda in item["resumen"].lower()
        coincide_tema = texto_busqueda in item["tema"].lower()
        if not (coincide_palabra or coincide_resumen or coincide_tema):
            continue

    resultados_filtrados.append(item)

st.markdown(f"**Resultados encontrados:** {len(resultados_filtrados)}")
st.markdown("")

# --- VISUALIZACIÓN EN TARJETAS (CARDS) ---
if not resultados_filtrados:
    st.info(
        "No se encontraron contenidos con esos filtros. Probá cambiando los"
        " criterios."
    )
else:
    for i in range(0, len(resultados_filtrados), 2):
        col1, col2 = st.columns(2)

        # Tarjeta 1
        with col1:
            item = resultados_filtrados[i]
            with st.container(border=True):
                st.markdown(f"### {item['nombre']} — *{item['canal']}*")
                st.markdown(f"**Tema:** {item['tema']}")
                st.markdown(f"**Opinión:** `{item['opinion']}`")
                st.markdown(f"**Resumen:** {item['resumen']}")

                tags_html = " ".join(
                    [
                        f"<span"
                        f" style='background-color:#e0f2fe;color:#0369a1;padding:2px"
                        f" 8px;border-radius:4px;font-size:12px;'>#{p}</span>"
                        for p in item["palabras_clave"]
                    ]
                )
                st.markdown(tags_html, unsafe_allow_html=True)
                st.markdown("")
                st.markdown(f"[Ir al contenido original 🔗]({item['link']})")

                st.markdown("---")
                st.markdown("📌 *Contenidos relacionados:*")
                relacionados = [
                    otro
                    for otro in corpus_literario
                    if otro["nombre"] != item["nombre"]
                    and any(
                        p in otro["palabras_clave"] for p in item["palabras_clave"]
                    )
                ]
                if relacionados:
                    for rel in relacionados[:2]:
                        st.markdown(
                            f"- [{rel['nombre']}: {rel['tema']}]({rel['link']})"
                        )
                else:
                    st.markdown("_No hay relaciones directas aún._")

        # Tarjeta 2 (si existe en la dupla)
        if i + 1 < len(resultados_filtrados):
            with col2:
                item = resultados_filtrados[i + 1]
                with st.container(border=True):
                    st.markdown(f"### {item['nombre']} — *{item['canal']}*")
                    st.markdown(f"**Tema:** {item['tema']}")
                    st.markdown(f"**Opinión:** `{item['opinion']}`")
                    st.markdown(f"**Resumen:** {item['resumen']}")

                    tags_html = " ".join(
                        [
                            f"<span"
                            f" style='background-color:#e0f2fe;color:#0369a1;padding:2px"
                            f" 8px;border-radius:4px;font-size:12px;'>#{p}</span>"
                            for p in item["palabras_clave"]
                        ]
                    )
                    st.markdown(tags_html, unsafe_allow_html=True)
                    st.markdown("")
                    st.markdown(
                        f"[Ir al contenido original 🔗]({item['link']})"
                    )

                    st.markdown("---")
                    st.markdown("📌 *Contenidos relacionados:*")
                    relacionados = [
                        otro
                        for otro in corpus_literario
                        if otro["nombre"] != item["nombre"]
                        and any(
                            p in otro["palabras_clave"]
                            for p in item["palabras_clave"]
                        )
                    ]
                    if relacionados:
                        for rel in relacionados[:2]:
                            st.markdown(
                                f"- [{rel['nombre']}:"
                                f" {rel['tema']}]({rel['link']})"
                            )
                    else:
                        st.markdown("_No hay relaciones directas aún._")

# --- SECCIÓN 3: TOP 10 Y MAPA DE RED DISCURSIVA ---
st.markdown("---")
st.subheader("🌐 Cartografía de Relaciones y Tendencias del Corpus")

col_i, col_d = st.columns(2)

with col_i:
    st.markdown("### 🏆 Top Temas y Autores")
    st.markdown(
        "_Los ejes temáticos y figuras más recurrentes en el corpus analizado._"
    )

    conteo_temas = {}
    for item in corpus_literario:
        t = item["tema"]
        conteo_temas[t] = conteo_temas.get(t, 0) + 1

    temas_ordenados = sorted(
        conteo_temas.items(), key=lambda x: x[1], reverse=True
    )[:10]

    for i, (tema, cantidad) in enumerate(temas_ordenados, 1):
        st.markdown(f"**{i}. {tema}** — `({cantidad} menciones)`")

with col_d:
    st.markdown("### 🧠 Mapa de Red Discursiva")
    st.markdown("_Conexiones cruzadas entre conceptos clave del campo._")

    st.info(
        "💡 **Nodo Central Activo:** El campo se articula en torno a tres"
        " grandes constelaciones de sentido:"
    )

    st.markdown(
        """
    - 🔴 **Eje Terror / Conurbano:** Vincula a *Mariana Enríquez* con *Samanta Schweblin* a través de etiquetas como `#siniestro`, `#atmósfera` y `#distopía`.
    - 🔵 **Eje Canon / Memoria:** Conecta a *Fogwill* con los debates sobre la dictadura y el `#humor_negro`.
    - 🟢 **Eje Crítica Contemporánea:** Agrupa las discusiones sobre la legibilidad de los clásicos (ej. *James Joyce*) en plataformas digitales.
    """
    )

    palabra_a_explorar = st.selectbox(
        "Seleccioná una etiqueta para ver su red de nodos:",
        ["#terror", "#canon_argentino", "#atmósfera", "#ficción"],
    )

    relacionados_red = [
        item
        for item in corpus_literario
        if any(
            palabra_a_explorar.replace("#", "") in p.lower()
            for p in item["palabras_clave"]
        )
    ]

    if relacionados_red:
        st.markdown(
            f"**Contenidos vinculados a `{palabra_a_explorar}`:**"
        )
        for rel in relacionados_red:
            st.markdown(
                f"- 🔗 **{rel['nombre']}** ({rel['canal']}): _{rel['tema']}_"
            )
    else:
        st.markdown("_No hay conexiones directas en esta muestra._")
