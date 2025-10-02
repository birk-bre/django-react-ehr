import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { patientAPI } from '../api'

function Patients() {
  const [patients, setPatients] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    medical_record_number: '',
    first_name: '',
    last_name: '',
    date_of_birth: '',
    gender: 'M',
    blood_type: '',
    phone: '',
    email: '',
    address: '',
    emergency_contact_name: '',
    emergency_contact_phone: '',
  })

  useEffect(() => {
    loadPatients()
  }, [])

  const loadPatients = async () => {
    try {
      const response = await patientAPI.getAll()
      setPatients(response.data)
    } catch (error) {
      console.error('Error loading patients:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await patientAPI.create(formData)
      setShowForm(false)
      setFormData({
        medical_record_number: '',
        first_name: '',
        last_name: '',
        date_of_birth: '',
        gender: 'M',
        blood_type: '',
        phone: '',
        email: '',
        address: '',
        emergency_contact_name: '',
        emergency_contact_phone: '',
      })
      loadPatients()
    } catch (error) {
      console.error('Error creating patient:', error)
      alert('Error creating patient')
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  if (loading) return <div className="loading">Loading...</div>

  return (
    <div className="patients-page">
      <div className="page-header">
        <h2>Patients</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'Add Patient'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="patient-form">
          <div className="form-grid">
            <input name="medical_record_number" placeholder="Medical Record Number" onChange={handleChange} value={formData.medical_record_number} required />
            <input name="first_name" placeholder="First Name" onChange={handleChange} value={formData.first_name} required />
            <input name="last_name" placeholder="Last Name" onChange={handleChange} value={formData.last_name} required />
            <input name="date_of_birth" type="date" onChange={handleChange} value={formData.date_of_birth} required />
            <select name="gender" onChange={handleChange} value={formData.gender} required>
              <option value="M">Male</option>
              <option value="F">Female</option>
              <option value="O">Other</option>
            </select>
            <select name="blood_type" onChange={handleChange} value={formData.blood_type}>
              <option value="">Select Blood Type</option>
              <option value="A+">A+</option>
              <option value="A-">A-</option>
              <option value="B+">B+</option>
              <option value="B-">B-</option>
              <option value="AB+">AB+</option>
              <option value="AB-">AB-</option>
              <option value="O+">O+</option>
              <option value="O-">O-</option>
            </select>
            <input name="phone" placeholder="Phone" onChange={handleChange} value={formData.phone} required />
            <input name="email" type="email" placeholder="Email" onChange={handleChange} value={formData.email} />
            <input name="address" placeholder="Address" onChange={handleChange} value={formData.address} required />
            <input name="emergency_contact_name" placeholder="Emergency Contact Name" onChange={handleChange} value={formData.emergency_contact_name} required />
            <input name="emergency_contact_phone" placeholder="Emergency Contact Phone" onChange={handleChange} value={formData.emergency_contact_phone} required />
          </div>
          <button type="submit" className="btn-primary">Create Patient</button>
        </form>
      )}

      <div className="patients-list">
        {patients.map(patient => (
          <Link key={patient.id} to={`/patient/${patient.id}`} className="patient-card">
            <h3>{patient.first_name} {patient.last_name}</h3>
            <p>MRN: {patient.medical_record_number}</p>
            <p>DOB: {patient.date_of_birth}</p>
            <p>Phone: {patient.phone}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default Patients
