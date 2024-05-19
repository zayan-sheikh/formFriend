import { Link } from 'react-router-dom'

const Navbar = () => {
return (
    <header>
        <div className="navBar">
            <Link className="navLink" to="/">
                <h1>formFriend</h1>
            </Link>
        </div>

        <div className="underlayBar"/>
    </header>
)}
export default Navbar