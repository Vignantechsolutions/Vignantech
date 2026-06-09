import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import API from '../api/client';
import toast from 'react-hot-toast';

export default function Register() {
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({ first_name:'', last_name:'', email:'', phone:'', password:'' });
  const [otp, setOtp] = useState('');
  const [pending, setPending] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await API.post('/auth/register/', form);
      setPending(data.pending);
      toast.success(`OTP sent to ${form.email}`);
      setStep(2);
    } catch (err) {
      const errors = err.response?.data;
      toast.error(errors?.email?.[0] || errors?.password?.[0] || 'Registration failed.');
    } finally { setLoading(false); }
  };

  const handleVerify = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await API.post('/auth/verify-otp/', { email: form.email, otp, pending });
      localStorage.setItem('access', data.access);
      localStorage.setItem('refresh', data.refresh);
      toast.success('Account created! Welcome to Vignan TechSolutions.');
      navigate('/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Invalid OTP.');
    } finally { setLoading(false); }
  };

  return (
    <div style={s.page}>
      <div style={s.card}>
        {step === 1 ? (
          <>
            <h2 style={s.title}>Create Account</h2>
            <p style={s.sub}>Join Vignan TechSolutions — Free</p>
            <form onSubmit={handleRegister}>
              <div style={s.row}>
                <div style={{flex:1}}>
                  <label style={s.label}>First Name</label>
                  <input style={s.input} value={form.first_name} onChange={e => setForm({...form, first_name:e.target.value})} required placeholder="John" />
                </div>
                <div style={{flex:1}}>
                  <label style={s.label}>Last Name</label>
                  <input style={s.input} value={form.last_name} onChange={e => setForm({...form, last_name:e.target.value})} required placeholder="Doe" />
                </div>
              </div>
              <label style={s.label}>Email Address</label>
              <input style={s.input} type="email" value={form.email} onChange={e => setForm({...form, email:e.target.value})} required placeholder="you@example.com" />
              <label style={s.label}>Phone Number</label>
              <input style={s.input} value={form.phone} onChange={e => setForm({...form, phone:e.target.value})} required placeholder="+91 9876543210" />
              <label style={s.label}>Password</label>
              <input style={s.input} type="password" value={form.password} onChange={e => setForm({...form, password:e.target.value})} required minLength={8} placeholder="Min. 8 characters" />
              <button type="submit" style={s.btn} disabled={loading}>{loading ? 'Sending OTP...' : 'Create Account'}</button>
            </form>
          </>
        ) : (
          <>
            <h2 style={s.title}>Verify Your Email</h2>
            <p style={s.sub}>We sent a 6-digit OTP to <strong>{form.email}</strong></p>
            <form onSubmit={handleVerify}>
              <label style={s.label}>Enter OTP</label>
              <input style={{...s.input, textAlign:'center', letterSpacing:'1rem', fontSize:'1.5rem'}}
                value={otp} onChange={e => setOtp(e.target.value)} required maxLength={6} placeholder="------" />
              <button type="submit" style={s.btn} disabled={loading}>{loading ? 'Verifying...' : 'Verify & Continue'}</button>
            </form>
            <button onClick={() => setStep(1)} style={s.back}>← Change Email</button>
          </>
        )}
        <p style={s.footer}>Already have an account? <Link to="/login" style={s.link}>Sign In</Link></p>
      </div>
    </div>
  );
}

const s = {
  page: { minHeight:'80vh', display:'flex', alignItems:'center', justifyContent:'center', background:'#F8FAFC', padding:'2rem' },
  card: { background:'#fff', borderRadius:20, padding:'2.5rem', width:'100%', maxWidth:480, boxShadow:'0 8px 32px rgba(0,0,0,.08)' },
  title: { fontWeight:800, fontSize:'1.75rem', color:'#0F172A', marginBottom:'.25rem' },
  sub: { color:'#6B7280', fontSize:'.9rem', marginBottom:'2rem' },
  row: { display:'flex', gap:'1rem' },
  label: { display:'block', fontWeight:600, fontSize:'.85rem', color:'#374151', marginBottom:'.4rem' },
  input: { width:'100%', border:'1.5px solid #E2E8F0', borderRadius:10, padding:'.7rem 1rem', fontSize:'.95rem', marginBottom:'1rem', boxSizing:'border-box', outline:'none' },
  btn: { width:'100%', background:'linear-gradient(135deg,#1E3A8A,#3B82F6)', color:'#fff', border:'none', borderRadius:10, padding:'.85rem', fontSize:'1rem', fontWeight:700, cursor:'pointer', marginTop:'.5rem' },
  back: { background:'none', border:'none', color:'#6B7280', cursor:'pointer', marginTop:'1rem', fontSize:'.9rem' },
  footer: { textAlign:'center', marginTop:'1.5rem', color:'#6B7280', fontSize:'.9rem' },
  link: { color:'#1E3A8A', fontWeight:700, textDecoration:'none' },
};
