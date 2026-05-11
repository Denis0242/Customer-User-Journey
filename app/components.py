import streamlit as st

def decision_panel():
    st.subheader("Insight → Action → Recommendation → Decision")
    st.markdown(
        """
        **Insight:** Users progress well through early funnel stages, but checkout-to-purchase creates visible friction.  
        **Action:** Analyze checkout friction by device, country, and segment.  
        **Recommendation:** Improve checkout UX, speed, payment trust signals, and retention messaging for at-risk users.  
        **Decision:** Prioritize checkout optimization before scaling acquisition spend.
        """
    )
