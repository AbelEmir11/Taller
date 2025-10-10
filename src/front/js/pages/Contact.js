import React from 'react';
import heroImg from "../../img/hero-img.png";
import worldDottedMap from "../../img/world-dotted-map.png";
import "../../styles/home.css";

const Contact = () => {

  const handleEmailClick = () => {
    window.location.href = "mailto:info@example.com";
  };

  return (
    <>
      <section id="hero" className="hero section dark-background snipcss-OOBoC">
        <img
          src={worldDottedMap}
          alt=""
          className="hero-bg aos-init aos-animate"
          data-aos="fade-in"
        />
        <div className="container">
          <div className="row gy-4 d-flex justify-content-between">
            <div className="col-lg-6 order-2 order-lg-1 d-flex flex-column justify-content-center">
              <button
                onClick={handleEmailClick}
                className="btn btn-primary w-100 p-3 fw-bold"
              >
                Contacta con nosotros
              </button>
              <img src={heroImg} className="img-fluid mb-3 mb-lg-0 imgContact" alt="" />
            </div>
            <div
              className="col-lg-5 order-1 order-lg-2 hero-img aos-init aos-animate"
              data-aos="zoom-out"
            >
              <h2 data-aos="fade-up" className="aos-init aos-animate">
                Nuestra ubicacion
              </h2>
              <iframe
                src="https://maps.app.goo.gl/1vEBzeqNWdMp2UkQ9"
                width="600"
                height="450"
                style={{border:0}}
                allowfullscreen=""
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
              ></iframe>
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default Contact;
