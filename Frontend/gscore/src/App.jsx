import React, { useReducer } from 'react';
import { Route, Routes } from 'react-router-dom';
import './App.css';
import Footer from './components/layout/Footer';
import Header from './components/layout/Header';
import StudentExamResult from './components/resultCheck';
import { MyUserContext } from './configs/context';
import MyUserReducer from './reducers/myReducer';

function App() {
  const [user, dispatch] = useReducer(MyUserReducer, null);

  return (
    <MyUserContext.Provider value={[user, dispatch]}>
      <Header />
      <div className="container">
        <Routes>
          <Route path="/" element={<h1>Welcome to G-Score</h1>} />
          <Route path="/result" element={<StudentExamResult />} />
        </Routes>
      </div>
      <Footer />
    </MyUserContext.Provider>
  );
}

export default App;
