import streamlit as st
import dhlab.nbtext as nb
import pandas as pd
from PIL import Image


image = Image.open('NB-logo-no-eng-svart.png')
st.image(image, width = 200)
st.markdown('Se mer om å drive analytisk DH på [DHLAB-siden](https://nbviewer.jupyter.org/github/DH-LAB-NB/DHLAB/blob/master/DHLAB_ved_Nasjonalbiblioteket.ipynb), og korpusanalyse via web [her](https://beta.nb.no/korpus/)')


st.title('Sjekk ord i bøker')

st.markdown('### Input')
words = st.text_input('Skriv inn ordene som skal sjekkes adskilt med komma','')
wordlist = [x.strip() for x in words.split(',')]

ddk = st.text_input('Deweynummer - skriv bare de første sifrene', "")
if ddk == "":
    ddk = None

if ddk != None and not ddk.endswith("%"):
    ddk = ddk + "%"

antall = st.number_input( 'Antall bøker - jo fler jo lenger ventetid, forskjellige søk vil vanligvis gi nye bøker (trykk på +/- for starte nye søk', 10)    

period_slider = st.slider(
    'Angi periode - år mellom 1900 og 2014',
    1900, 2020, (1950, 2010)
)


if words != "":
    urns = {w:nb.book_urn(words=[w], ddk = ddk, period = (period_slider[0], period_slider[1]), limit = antall) for w in wordlist}
    data = {w: nb.aggregate_urns(urns[w]) for w in wordlist}

    df = pd.concat([nb.frame(data[w], 'bok_' + w) for w in wordlist], axis = 1)
    
    st.markdown("### Bøker som inneholder en av _{ws}_ i kolonnene, ordfrekvens i radene".format(ws = ', '.join(wordlist)))
    st.write('En diagonal indikerer at ordene gjensidig utelukker hverandre')
    st.write(df.loc[wordlist].fillna(0))

    
