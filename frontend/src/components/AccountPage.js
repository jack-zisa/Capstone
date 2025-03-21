import React, { useState } from 'react';

function AccountPage() {
  const [gender, setGender] = useState('');
  const [age, setAge] = useState(1);
  const [weight, setWeight] = useState(0.0);
  const [height, setHeight] = useState(0.0);

  const handleSubmit = async (e) => {
    e.preventDefault();  // Prevents the form from refreshing the page

    const data = {
      gender,
      age,
      weight,
      height,
    };

    try {
      const response = await fetch('/user/demographics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        // Handle success response
        const result = await response.json();
        console.log('Form submitted successfully', result);
      } else {
        // Handle error response
        console.error('Failed to submit form', response.status);
      }
    } catch (error) {
      // Handle network or other errors
      console.error('Error submitting form', error);
    }
  };

  return (
    <div className="AccountPage">
      <h2>Account</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="gender">Gender</label>
          <select name="gender" id="gender" value={gender} onChange={(e) => setGender(e.target.value)}>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div>
          <label htmlFor="age">Age</label>
          <input type="number" id="age" value={age} onChange={(e) => setAge(e.target.value)} min="1"/>
        </div>
        <div>
          <label htmlFor="weight">Weight</label>
          <input type="number" id="weight" value={weight} onChange={(e) => setWeight(e.target.value)} min="0" step="0.1"/>
        </div>
        <div>
          <label htmlFor="height">Height</label>
          <input type="number" id="height" value={height} onChange={(e) => setHeight(e.target.value)} min="0" step="0.1"/>
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default AccountPage;
