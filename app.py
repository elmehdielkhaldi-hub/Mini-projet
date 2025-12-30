import streamlit as st
import pandas as pd
from Models.gestion_conge import GestionConges

st.set_page_config(page_title="Gestion des congés", layout="wide")
gc = GestionConges()

# Titre avec icône
st.markdown("# :material/calendar_month: Gestion des congés")

menu = st.sidebar.selectbox(
    "Menu",
    ["Employés", "Nouvelle demande", "Demandes", "Validation RH"]
)

# ---------- EMPLOYÉS ----------
if menu == "Employés":
    st.markdown("### :material/person_add: Ajouter un employé")
    col1, col2, col3 = st.columns(3)
    with col1:
        m = st.text_input("Matricule", key="matricule", placeholder="ID employé")
        n = st.text_input("Nom", key="nom")
    with col2:
        p = st.text_input("Prénom", key="prenom")
        s = st.text_input("Service", key="service")
    with col3:
        solde = st.number_input("Solde congés", 0, 30, 22)

    if st.button("Ajouter", use_container_width=True):
        gc.ajouter_employe(m, n, p, s, solde)
        st.success(":material/check: Employé ajouté avec succès")

    # Recharge toujours le tableau
    employes = gc.lister_employes()
    if employes:
        st.markdown("### :material/list: Liste des employés")
        df_emp = pd.DataFrame(employes)
        st.dataframe(df_emp, use_container_width=True)
    else:
        st.info(":material/info: Aucun employé enregistré")

# ---------- NOUVELLE DEMANDE ----------
elif menu == "Nouvelle demande":
    st.markdown("### :material/edit_note: Nouvelle demande de congé")
    employes = gc.lister_employes()
    if not employes:
        st.warning(":material/warning: Aucun employé disponible")
    else:
        choix = {f"{e['nom']} {e['prenom']}": e["id"] for e in employes}
        emp = st.selectbox("Employé", choix.keys())
        d1 = st.date_input("Date début")
        d2 = st.date_input("Date fin")
        t = st.selectbox("Type", ["Annuel", "Exceptionnel", "Maladie"])
        c = st.text_area("Commentaire")
        if st.button("Envoyer la demande", use_container_width=True):
            gc.ajouter_demande(
                choix[emp],
                d1.strftime("%Y-%m-%d"),
                d2.strftime("%Y-%m-%d"),
                t,
                c
            )
            st.success(":material/check: Demande envoyée avec succès")

# ---------- TOUTES LES DEMANDES ----------
elif menu == "Demandes":
    st.markdown("### :material/assignment: Toutes les demandes")
    demandes = gc.lister_demandes()
    if demandes:
        st.dataframe(pd.DataFrame(demandes), use_container_width=True)
    else:
        st.info(":material/info: Aucune demande enregistrée")

# ---------- VALIDATION RH ----------
elif menu == "Validation RH":
    st.markdown("### :material/pending: Demandes en attente")
    demandes = gc.lister_demandes("En attente")

    if not demandes:
        st.success(":material/check: Aucune demande en attente")
    else:
        for d in demandes:
            with st.container():
                st.markdown("---")
                cols = st.columns([2,2,2,2])
                cols[0].markdown(f":material/person: **Employé ID:** {d['employe_id']}")
                cols[1].markdown(f":material/date_range: **Période:** {d['date_debut']} → {d['date_fin']}")
                cols[2].markdown(f":material/category: **Type:** {d['type_conge']}")

                col_buttons = st.columns(2)
                
                # Accepter
                with col_buttons[0]:
                    if st.button("Accepter", key=f"a{d['id']}", use_container_width=True, type="primary"):
                        statut = gc.traiter_demande(d["id"], True)
                        if statut == "Accepté":
                            st.success(":material/check: Demande acceptée")
                        else:
                            st.warning(":material/warning: Solde insuffisant")
                        # Recharge tableau Employés automatiquement
                        employes = gc.lister_employes()
                        st.dataframe(pd.DataFrame(employes), use_container_width=True)

                # Refuser
                with col_buttons[1]:
                    if st.button("Refuser", key=f"r{d['id']}", use_container_width=True):
                        gc.traiter_demande(d["id"], False)
                        st.warning(":material/cancel: Demande refusée")
                        # Recharge tableau Employés
                        employes = gc.lister_employes()
                        st.dataframe(pd.DataFrame(employes), use_container_width=True)