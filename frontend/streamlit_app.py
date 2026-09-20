import os
import requests
import streamlit as st


API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


st.set_page_config(
    page_title="Prior Authorization AI",
    page_icon="🏥",
    layout="wide",
)


st.title("🏥 Prior Authorization AI")
st.caption(
    "AI-powered prior authorization processing system"
)

st.divider()


st.subheader("Upload Authorization Document")

uploaded_file = st.file_uploader(
    "Upload a PDF, image, or text document",
    type=["pdf", "png", "jpg", "jpeg", "txt"],
)


if uploaded_file is not None:

    st.write(
        f"**Selected:** {uploaded_file.name}"
    )

    if st.button(
        "Process Authorization",
        type="primary"
    ):

        with st.spinner(
            "Processing authorization..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/api/authorizations",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type,
                        )
                    },
                    timeout=120,
                )

                if response.status_code == 200:
                    result = response.json()

                    st.session_state["result"] = result

                else:
                    st.error(
                        f"API error: {response.status_code}"
                    )

                    st.code(
                        response.text
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the FastAPI server. "
                    "Make sure FastAPI is running on port 8000."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "The request timed out."
                )

            except Exception as error:
                st.error(
                    f"Unexpected error: {error}"
                )


if "result" in st.session_state:

    result = st.session_state["result"]

    st.divider()

    st.subheader("Authorization Result")

    if result["status"] == "SUCCESS":

        st.success(
            "Authorization processed successfully."
        )

        authorization = result["authorization"]
        validation = result["validation"]
        submission = result["submission"]
        tracking = result["tracking"]

        # -------------------------
        # Patient / Request details
        # -------------------------

        st.subheader("Request Details")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Patient",
                authorization["patient"]["name"]
            )

        with col2:
            st.metric(
                "Procedure",
                authorization["procedure"]["description"]
            )

        with col3:
            st.metric(
                "Payer",
                authorization["payer"]["name"]
            )

        st.write(
            "**Provider:**",
            authorization["provider"]["name"]
        )

        st.write(
            "**Diagnosis:**",
            authorization["diagnosis"]["description"]
        )

        # -------------------------
        # Clinical notes
        # -------------------------

        with st.expander("Clinical Notes"):

            st.write(
                authorization.get(
                    "clinical_notes",
                    ""
                )
            )

        # -------------------------
        # Validation
        # -------------------------

        st.subheader("Validation")

        if validation["status"] == "VALID":
            st.success("✓ VALID")
        else:
            st.error("✗ INVALID")

        if validation["warnings"]:

            st.warning(
                "Warnings detected"
            )

            for warning in validation["warnings"]:
                st.write(
                    f"⚠️ {warning}"
                )

        if validation["errors"]:

            st.error(
                "Validation errors"
            )

            for error in validation["errors"]:
                st.write(
                    f"❌ {error}"
                )

        # -------------------------
        # Submission
        # -------------------------

        st.subheader("Submission")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Submission ID",
                submission["submission_id"]
            )

        with col2:
            st.metric(
                "Status",
                submission["status"]
            )

        # -------------------------
        # Tracking
        # -------------------------

        st.subheader("Tracking")

        st.info(
            f"Current Status: "
            f"{tracking['current_status']}"
        )

    else:

        st.error(
            f"Processing failed: {result['status']}"
        )

        if "stage" in result:
            st.write(
                f"**Failed Stage:** {result['stage']}"
            )

        if "error" in result:
            st.code(
                result["error"]
            )
st.divider()

st.subheader("🔍 Track Authorization")
st.subheader("🤖 Agent Pipeline")

agent_activity = result.get("agent_activity", [])

for activity in agent_activity:
    agent_name = activity["agent"]
    status = activity["status"]
    message = activity["message"]

    if status in {"COMPLETED", "VALID", "SUBMITTED", "TRACKING"}:
        st.success(
            f"✅ {agent_name} — {status}\n\n"
            f"{message}"
        )
    else:
        st.error(
            f"❌ {agent_name} — {status}\n\n"
            f"{message}"
        )

submission_id = st.text_input(
    "Enter Submission ID",
    placeholder="Example: AUTH-0A981D8A",
)

if st.button("Track Authorization"):
    if not submission_id.strip():
        st.warning("Please enter a submission ID.")
    else:
        with st.spinner("Fetching authorization status..."):
            try:
                response = requests.get(
                    f"{API_URL}/api/authorizations/{submission_id.strip()}",
                    timeout=30,
                )

                if response.status_code == 200:
                    tracking = response.json()

                    st.success("Authorization found.")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Patient",
                            tracking["patient_name"],
                        )

                    with col2:
                        st.metric(
                            "Payer",
                            tracking["payer"],
                        )

                    with col3:
                        st.metric(
                            "Status",
                            tracking["current_status"],
                        )

                    st.write(
                        "**Procedure:**",
                        tracking["procedure"],
                    )

                    st.write(
                        "**Submission ID:**",
                        tracking["submission_id"],
                    )

                    st.write(
                        "**Submitted At:**",
                        tracking["submitted_at"],
                    )

                    st.write(
                        "**Last Updated:**",
                        tracking["updated_at"],
                    )

                elif response.status_code == 404:
                    st.error("Authorization not found.")

                else:
                    st.error(
                        f"API error: {response.status_code}"
                    )
                    st.code(response.text)

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the FastAPI server. "
                    "Make sure FastAPI is running on port 8000."
                )

            except requests.exceptions.Timeout:
                st.error("The request timed out.")

            except Exception as error:
                st.error(f"Unexpected error: {error}")