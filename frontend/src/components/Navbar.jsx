import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => { logout(); navigate('/'); };

  return (
    <nav style={styles.nav}>
      <div style={styles.container}>
        <Link to="/" style={styles.brand}>Vignan TechSolutions</Link>
        <div style={styles.links}>
          <Link to="/" style={styles.link}>Home</Link>
          <Link to="/about" style={styles.link}>About</Link>
          <Link to="/projects" style={styles.link}>Projects</Link>
          <Link to="/internships" style={styles.link}>Internships</Link>
          <Link to="/courses" style={styles.link}>Courses</Link>
          <Link to="/contact" style={styles.link}>Contact</Link>
          {user ? (
            <>
              <Link to="/dashboard" style={styles.link}>{user.name?.split(' ')[0]}</Link>
              <button onClick={handleLogout} style={styles.btn}>Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" style={styles.link}>Login</Link>
              <Link to="/register" style={{...styles.btn, textDecoration:'none'}}>Register Free</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

const styles = {
  nav: { background:'#fff', boxShadow:'0 2px 12px rgba(0,0,0,.08)', position:'sticky', top:0, zIndex:100 },
  container: { maxWidth:1200, margin:'0 auto', padding:'0 1.5rem', display:'flex', alignItems:'center', justifyContent:'space-between', height:64 },
  brand: { fontWeight:800, fontSize:'1.1rem', color:'#1E3A8A', textDecoration:'none' },
  links: { display:'flex', alignItems:'center', gap:'1.25rem' },
  link: { color:'#374151', textDecoration:'none', fontSize:'.9rem', fontWeight:500 },
  btn: { background:'linear-gradient(135deg,#1E3A8A,#3B82F6)', color:'#fff', border:'none', borderRadius:50, padding:'.4rem 1.1rem', fontSize:'.85rem', fontWeight:700, cursor:'pointer' },
};
