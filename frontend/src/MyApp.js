import React, {useState, useEffect} from 'react';
import Table from './Table';
import Form from './Form';
import axios from 'axios';

function MyApp() {
const [characters, setCharacters] = useState([]);
useEffect(() => {
  fetchAll().then( result => {
     if (result)
        setCharacters(result);
   });
}, [] );

async function removeOneCharacter (index) {
  const userID = characters[index].id
  const url = 'http://localhost:5000/users/'+ userID
  const res = await axios.delete(url)
  if (res && (res.status === 204)){
     const updated = characters.filter((character, i) => {
     return i !== index
     });
   setCharacters(updated);
   return res
  }
  if(res && (res.status === 404)){
     console.log("resource not found")
  }
  return res
  }

  async function fetchAll(){
    try {
       const response = await axios.get('http://localhost:5000/users');
       return response.data.users_list;     
    }
    catch (error){
       //We're not handling errors. Just logging into the console.
       console.log(error); 
       return false;         
    }
 }

 async function makePostCall(person){
  try {
     const response = await axios.post('http://localhost:5000/users', person);
     return response;
  }
  catch (error) {
     console.log(error);
     return false;
  }
}

function updateList(person) { 
  makePostCall(person).then( result => {
  if (result && (result.status === 201))
     setCharacters([...characters, result.data] );
  });
}

return (
  <div className="container">
    <Table characterData={characters} removeCharacter={removeOneCharacter} />
    <Form handleSubmit={updateList} />
  </div>
)
}
export default MyApp;