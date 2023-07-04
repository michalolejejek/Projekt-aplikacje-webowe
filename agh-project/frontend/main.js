import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

//wyswietlanie listy klientów
function CustomerList({ customers }) {
  return (
    <div>
      <h1>Lista klientów</h1>
      <ul>
        {customers.map((customer) => (
          <li key={customer.id}>
            {customer.name} {customer.surname}
          </li>
        ))}
      </ul>
    </div>
  );
}

//pobieralnie listy klientów z  api
async function fetchCustomers() {
  try {
    const response = await axios.get('/customers');
    return response.data;
  } catch (error) {
    console.error('Wystąpił błąd podczas pobierania listy klientów:', error);
    return [];
  }
}

async function main() {
  const customers = await fetchCustomers();
  ReactDOM.render(
    <CustomerList customers={customers} />,
    document.getElementById('root')
  );
}

main();
