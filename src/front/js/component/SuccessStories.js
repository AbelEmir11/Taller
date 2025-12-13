import React, { useState, useEffect } from "react";
import "../../styles/success_stories.css";

export const SuccessStories = () => {
    const [stories, setStories] = useState([]);
    const [loading, setLoading] = useState(true);
    const apiUrl = process.env.BACKEND_URL + "/api";

    useEffect(() => {
        loadSuccessStories();
    }, []);

    const loadSuccessStories = async () => {
        try {
            const response = await fetch(`${apiUrl}/success-stories?featured=true&limit=3`);
            if (response.ok) {
                const data = await response.json();
                setStories(data);
            }
        } catch (error) {
            console.error("Error loading success stories:", error);
        } finally {
            setLoading(false);
        }
    };

    // Datos de ejemplo mientras no haya en la base de datos
    const exampleStories = [
        {
            id: 1,
            title: "Restauración Completa de Motor",
            vehicle_model: "Toyota Corolla 2015",
            service_type: "Reparación de Motor",
            description: "Motor completamente restaurado, nuevas piezas y rendimiento óptimo",
            client_testimonial: "¡Increíble trabajo! Mi auto funciona como nuevo",
            before_image_url: "/api/placeholder/engine-before",
            after_image_url: "/api/placeholder/engine-after"
        },
        {
            id: 2,
            title: "Pintura y Restauración de Chapa",
            vehicle_model: "Ford Focus 2018",
            service_type: "Pintura y Chapa",
            description: "Trabajo completo de pintura y reparación de abolladuras",
            client_testimonial: "Quedó perfecto, como de fábrica",
            before_image_url: "/api/placeholder/paint-before",
            after_image_url: "/api/placeholder/paint-after"
        },
        {
            id: 3,
            title: "Reemplazo de Suspensión",
            vehicle_model: "Honda Civic 2017",
            service_type: "Sistema de Suspensión",
            description: "Suspensión completa renovada para mejor confort de manejo",
            client_testimonial: "La diferencia es notable, excelente servicio",
            before_image_url: "/api/placeholder/suspension-before",
            after_image_url: "/api/placeholder/suspension-after"
        }
    ];

    const displayStories = stories.length > 0 ? stories : exampleStories;

    return (
        <section className="success-stories-section">
            <div className="container py-5">
                <div className="text-center mb-5">
                    <h2 className="section-title" data-aos="fade-up">
                        🏆 Casos de Éxito
                    </h2>
                    <p className="section-subtitle" data-aos="fade-up" data-aos-delay="100">
                        Conoce algunos de nuestros trabajos más destacados
                    </p>
                </div>

                {loading ? (
                    <div className="text-center">
                        <div className="spinner-border text-primary" role="status">
                            <span className="visually-hidden">Cargando...</span>
                        </div>
                    </div>
                ) : (
                    <div className="row g-4">
                        {displayStories.map((story, index) => (
                            <div
                                key={story.id}
                                className="col-md-4"
                                data-aos="fade-up"
                                data-aos-delay={index * 100}
                            >
                                <div className="success-story-card">
                                    <div className="story-badge">{story.service_type}</div>

                                    <div className="before-after-container">
                                        <div className="image-wrapper before">
                                            <div className="image-label">Antes</div>
                                            <div className="placeholder-image before-img">
                                                <span>🔧</span>
                                                <p>Antes de la reparación</p>
                                            </div>
                                        </div>
                                        <div className="divider-arrow">→</div>
                                        <div className="image-wrapper after">
                                            <div className="image-label">Después</div>
                                            <div className="placeholder-image after-img">
                                                <span>✨</span>
                                                <p>Después de la reparación</p>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="story-content">
                                        <h3 className="story-title">{story.title}</h3>
                                        <p className="story-vehicle">
                                            <i className="fas fa-car"></i> {story.vehicle_model}
                                        </p>
                                        <p className="story-description">{story.description}</p>

                                        {story.client_testimonial && (
                                            <div className="testimonial">
                                                <i className="fas fa-quote-left"></i>
                                                <p>{story.client_testimonial}</p>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                <div className="text-center mt-5" data-aos="fade-up">
                    <p className="cta-text">
                        ¿Quieres que tu vehículo sea nuestro próximo caso de éxito?
                    </p>
                    <button className="btn btn-primary btn-lg">
                        Agenda tu Cita Ahora
                    </button>
                </div>
            </div>
        </section>
    );
};
