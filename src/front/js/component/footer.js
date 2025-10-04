import React from "react";

export const Footer = () => (
  <footer className="footer mt-auto py-3 text-center bg-dark text-white">
    <div className="container">
      <p className="mb-0">
        Hecho por:  <i className="fa fa-heart text-danger"></i> by{" "}
        <a
          href="https://github.com/AbelEmir11"
          target="_blank"
          className="text-decoration-none text-white fw-bold"
        >
          Abel Alvarado | &nbsp;
        </a>
        <a
          href="https://github.com/StevenSanz"
          target="_blank"
          className="text-decoration-none text-white fw-bold"
        >
          Melanie Alvarado | &nbsp;
        </a>
        <a
          href="https://github.com/nunezweb"
          target="_blank"
          className="text-decoration-none text-white fw-bold"
        >
          Mayra Villegas
        </a>
      </p>
    </div>
  </footer>
);