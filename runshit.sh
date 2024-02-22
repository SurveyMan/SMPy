source .venv/bin/activate
pip install -r REQUIREMENTS.txt
# because i have butter fingers and just nuked my history FML

python -m surveyman.input \
    ./survey.json \
    qsf \
    --replacements \
    "&nbsp;-> " \
    "q://QID70/ChoiceTextEntryValue/1->your instance" \
    "&ndash;->–" \
    --skipids \
    QID86 \
    BL_5d4c2fb3vCiWk4K \
    BL_cSURw3ZgzbsVymi \
    BL_ehNOJQlLWNb4GBU \
    BL_3luGQUfPA78kTJ4 \
    BL_enfTLgam0zKTqcK \
    BL_2hka13jPBKmeswC \
    BL_0voR8qQ5IKuCpTw \
    BL_6h6vPhh56Qx1Oce \
    BL_4Iomdl89ZQYDKEm \
    BL_9KzhxWoOTu1mafs 