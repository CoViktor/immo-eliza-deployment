import streamlit as st

# Streamlit
st.write('Hello world')
st.text_input('Input something:')
x = st.text_input('Input something else:')
y = st.slider('Slide me:', 0, 10)
st.write(f'You typed: {x} and slided {y}')

st.write("# markdown works as well!")
st.write('## type st. and see what suggestions it gives')
st.button('Click me!')
st.checkbox('Check me!')
st.radio('Pick one:', ('Option 1', 'Option 2', 'Option 3'))
st.selectbox('Pick one:', ('Option 1', 'Option 2', 'Option 3'))

