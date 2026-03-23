
import streamlit as st
import pickle
import pandas as pd
import requests
import certifi

@st.cache_data
def load_pickle_from_url(url):
    response = requests.get(url)
    return pickle.loads(response.content)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
   
    data = requests.get(url, verify=certifi.where(), timeout=10)
    data = data.json()
    # response = requests.get(url, timeout=10, headers={"Connection": "close"})
    # data = response.json()
    
    poster_path = data.get['poster_path']
    # full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    # return full_path  
    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"
    
    
def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies_posters=[]
    recommended_movies=[]
    
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters   


# movies_dict=pickle.load(open('movie_dict.pkl','rb'))
# movies=pd.DataFrame(movies_dict)

# similarity=pickle.load(open('similarity.pkl','rb'))
movies_dict = load_pickle_from_url("https://drive.google.com/uc?id=1WjT97gyk6k8GITXZXVIJ0Wi7MZzHVT3B")
similarity = load_pickle_from_url("https://drive.google.com/uc?id=1Whlvl4OnjYHcL8pY83qCjvDNJd3X4mD2")

movies = pd.DataFrame(movies_dict)

st.title('MovieBaaz.com')

selected_movie_name=st.selectbox(
    'Which movie u watched',
    movies['title'].values
)

if st.button('Recommend'):
    names,poster=recommend(selected_movie_name)
    
    col1,col2,col3,col4,col5=st.columns(5)

    with col1:
        st.text(names[0])
        st.image (poster[0])
    with col2:
        st.text(names[1])
        st.image (poster[1])
    with col3:
        st.text(names[2])
        st. image (poster[2])
    with col4:
       st.text(names[3])
       st.image (poster[3])
    with col5:
        st.text(names[4])
        st.image (poster[4])


# https://api.themoviedb.org/3/movie/550?api_key=897c779e174e6f849706dfd63b877bfd


