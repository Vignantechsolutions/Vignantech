import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const user = await login(form.email, form.password);
      toast.success(`Welcome back, ${user.name?.split(' ')[0]}!`);
      navigate(user.is_staff ? '/admin' : '/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Invalid credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={s.page}>
      <div style={s.card}>
        <h2 style={s.title}>Welcome Back</h2>
        <p style={s.sub}>Sign in to your Vignan TechSolutions account</p>
        <form onSubmit={handleSubmit}>
          <label style={s.label}>Email Address</label>
          <input style={s.input} type="email" value={form.email} onChange={e => setForm({...form, email: e.target.value})} required placeholder="you@example.com" />
          <label style={s.label}>Password</label>
          <input style={s.input} type="password" value={form.password} onChange={e => setForm({...form, password: e.target.value})} required placeholder="••••••••" />
          <div style={{textAlign:'right', marginBottom:'1.25rem'}}>
            <Link to="/forgot-password" style={s.forgotLink}>Forgot password?</Link>
          </div>
          <button type="submit" style={s.btn} disabled={loading}>{loading ? 'Signing in...' : 'Sign In'}</button>
        </form>
        <p style={s.footer}>Don't have an account? <Link to="/register" style={s.link}>Register Free</Link></p>
      </div>
    </div>
  );
}

const s = {
  page: { minHeight:'80vh', display:'flex', alignItems:'center', justifyContent:'center', background:'#F8FAFC', padding:'2rem' },
  card: { background:'#fff', borderRadius:20, padding:'2.5rem', width:'100%', maxWidth:440, boxShadow:'0 8px 32px rgba(0,0,0,.08)' },
  title: { fontWeight:800, fontSize:'1.75rem', color:'#0F172A', marginBottom:'.25rem' },
  sub: { color:'#6B7280', fontSize:'.9rem', marginBottom:'2rem' },
  label: { display:'block', fontWeight:600, fontSize:'.85rem', color:'#374151', marginBottom:'.4rem' },
  input: { width:'100%', border:'1.5px solid #E2E8F0', borderRadius:10, padding:'.7rem 1rem', fontSize:'.95rem', marginBottom:'1rem', boxSizing:'border-box', outline:'none' },
  btn: { width:'100%', background:'linear-gradient(135deg,#1E3A8A,#3B82F6)', color:'#fff', border:'none', borderRadius:10, padding:'.85rem', fontSize:'1rem', fontWeight:700, cursor:'pointer' },
  footer: { textAlign:'center', marginTop:'1.5rem', color:'#6B7280', fontSize:'.9rem' },
  link: { color:'#1E3A8A', fontWeight:700, textDecoration:'none' },
  forgotLink: { color:'#3B82F6', fontSize:'.85rem', textDecoration:'none' },
};
