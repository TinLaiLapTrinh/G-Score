import { Container, Nav, Navbar } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Header = () => {
    return (
        <Navbar bg="light" expand="lg" className="shadow-sm">
            <Container>
                <Navbar.Toggle aria-controls="main-navbar-nav" />
                <Navbar.Collapse id="main-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link as={Link} to="/">
                            Trang chủ
                        </Nav.Link>
                        <Nav.Link as={Link} to="/result">
                            Tra cứu điểm thi
                        </Nav.Link>
                    </Nav>

                    <Nav>
                        <Nav.Link as={Link} to="/login" className="text-info">
                            Đăng nhập
                        </Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
};

export default Header;
