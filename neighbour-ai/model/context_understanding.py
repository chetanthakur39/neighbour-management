from pathlib import Path
import py_compile
import sys


INPUT_FILE = Path(
    sys.argv[1]
    if len(sys.argv) > 1
    else "api_server.py"
)

OUTPUT_FILE = Path(
    sys.argv[2]
    if len(sys.argv) > 2
    else "api_server_context_understanding.py"
)


text = INPUT_FILE.read_text(
    encoding="utf-8"
)


# ============================================================
# 1. ADD CONVERSATION CONTEXT HELPERS
# ============================================================

anchor = """# ============================================================
# ENTITY CONFIDENCE SETTINGS
# ============================================================
"""

context_helpers = """# ============================================================
# CONVERSATION CONTEXT
#
# Uses the existing per-session conversation history.
# It fills only missing State/JC values.
# Explicit State/JC values in the current command always win.
# ============================================================

def get_session_context(
    session_id
):

    if not session_id:

        return {}


    with SESSION_CONVERSATIONS_LOCK:

        conversation = (
            SESSION_CONVERSATIONS.get(
                session_id,
                {}
            )
        )


        if not isinstance(
            conversation,
            dict
        ):

            return {}


        return {

            "state":
                conversation.get(
                    "last_state"
                ),

            "jc":
                conversation.get(
                    "last_jc"
                )
        }


def resolve_conversation_context(
    session_id,
    analysis
):

    if not isinstance(
        analysis,
        dict
    ):

        return analysis


    entities = analysis.get(
        "entities"
    )


    if not isinstance(
        entities,
        dict
    ):

        return analysis


    state = entities.get(
        "state"
    )

    jc = entities.get(
        "jc"
    )


    # Explicit State/JC from the current command always wins.
    if state and jc:

        return analysis


    context = get_session_context(
        session_id
    )


    context_state = context.get(
        "state"
    )

    context_jc = context.get(
        "jc"
    )


    context_used = False


    if not state and context_state:

        entities["state"] = context_state

        context_used = True


    if not jc and context_jc:

        entities["jc"] = context_jc

        context_used = True


    if context_used:

        analysis["entities"] = entities

        analysis["context_used"] = True


        missing = analysis.get(
            "missing"
        )


        if isinstance(
            missing,
            list
        ):

            analysis["missing"] = [

                item

                for item in missing

                if str(item).lower()
                not in (
                    "state",
                    "jc"
                )
            ]


    return analysis


# ============================================================
# ENTITY CONFIDENCE SETTINGS
# ============================================================
"""

if "def resolve_conversation_context(" not in text:

    if anchor not in text:

        raise RuntimeError(
            "Could not find ENTITY CONFIDENCE SETTINGS insertion point."
        )


    text = text.replace(
        anchor,
        context_helpers,
        1
    )


# ============================================================
# 2. RESOLVE CONTEXT AFTER EXISTING NLP ANALYSIS
# ============================================================

confidence_anchor = """            # =================================================
            # ENTITY CONFIDENCE CLARIFICATION
            # =================================================
"""

context_block = """            # =================================================
            # CONVERSATION CONTEXT
            #
            # Fill only missing State/JC values from the same
            # session. Explicit NLP results are never overwritten.
            # =================================================

            analysis = resolve_conversation_context(

                session_id,

                analysis
            )


"""

if context_block.strip() not in text:

    if confidence_anchor not in text:

        raise RuntimeError(
            "Could not find ENTITY CONFIDENCE CLARIFICATION insertion point."
        )


    text = text.replace(
        confidence_anchor,
        context_block + confidence_anchor,
        1
    )


# ============================================================
# 3. SAVE + SYNTAX CHECK
# ============================================================

OUTPUT_FILE.write_text(
    text,
    encoding="utf-8"
)

py_compile.compile(
    str(OUTPUT_FILE),
    doraise=True
)

print("SUCCESS")
print("Updated file:", OUTPUT_FILE.resolve())
