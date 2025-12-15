import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../../styles/success_stories_page.css";

export const SuccessStoriesPage = () => {
    const [stories, setStories] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    const apiUrl = process.env.BACKEND_URL + "/api";

    useEffect(() => {
        loadSuccessStories();
    }, []);

    const loadSuccessStories = async () => {
        try {
            const response = await fetch(`${apiUrl}/success-stories`);
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
            description: "Motor completamente restaurado con nuevas piezas. El vehículo recuperó su rendimiento óptimo y eficiencia de combustible.",
            client_testimonial: "¡Increíble trabajo! Mi auto funciona como nuevo, no puedo creer la diferencia.",
        },
        {
            id: 2,
            title: "Pintura y Restauración de Chapa",
            vehicle_model: "Ford Focus 2018",
            service_type: "Pintura y Chapa",
            description: "Trabajo completo de pintura y reparación de abolladuras. El acabado quedó impecable.",
            client_testimonial: "Quedó perfecto, como recién salido de fábrica. Muy satisfecho con el resultado.",
        },
        {
            id: 3,
            title: "Reemplazo de Suspensión",
            vehicle_model: "Honda Civic 2017",
            service_type: "Sistema de Suspensión",
            description: "Suspensión completa renovada para mejor confort de manejo y seguridad en la conducción.",
            client_testimonial: "La diferencia es notable, excelente servicio y atención personalizada.",
        },
        {
            id: 4,
            title: "Reparación de Sistema Eléctrico",
            vehicle_model: "Volkswagen Golf 2016",
            service_type: "Sistema Eléctrico",
            description: "Diagnóstico y reparación completa del sistema eléctrico. Se solucionaron fallas en el tablero y luces.",
            client_testimonial: "Muy profesionales, encontraron el problema rápidamente y lo resolvieron.",
        },
        {
            id: 5,
            title: "Cambio de Frenos Completo",
            vehicle_model: "Chevrolet Cruze 2019",
            service_type: "Sistema de Frenos",
            description: "Reemplazo completo de discos, pastillas y líquido de frenos. Seguridad garantizada.",
            client_testimonial: "Ahora el auto frena perfecto, me siento mucho más seguro al conducir.",
        },
        {
            id: 6,
            title: "Mantenimiento Preventivo",
            vehicle_model: "Nissan Sentra 2020",
            service_type: "Mantenimiento",
            description: "Servicio de mantenimiento preventivo completo incluyendo cambio de aceite, filtros y revisión general.",
            client_testimonial: "Servicio excelente y a buen precio. Muy recomendable.",
        }
    ];

    const displayStories = stories.length > 0 ? stories : exampleStories;

    return (
        <div className="success-stories-page">
            {/* Hero Section */}
            <section className="hero-section">
                <div className="container">
                    <h1 className="hero-title">🏆 Casos de Éxito</h1>
                    <p className="hero-subtitle">
                        Conoce los trabajos que hemos realizado para nuestros clientes satisfechos
                    </p>
                </div>
            </section>

            {/* Stories Grid */}
            <section className="stories-section">
                <div className="container py-5">
                    {loading ? (
                        <div className="text-center">
                            <div className="spinner-border text-primary" role="status">
                                <span className="visually-hidden">Cargando...</span>
                            </div>
                        </div>
                    ) : (
                        <div className="row g-4">
                            {displayStories.map((story, index) => (
                                <div key={story.id} className="col-md-6 col-lg-4">
                                    <div className="story-card">
                                        <div className="story-badge">{story.service_type}</div>

                                        <div className="before-after-container">
                                            <div className="image-wrapper">
                                                <div className="image-label">Antes / Después</div>
                                                <div className="placeholder-grid">
                                                    <div className="placeholder-box before">
                                                        <span className="icon">🔧</span>
                                                        <p>Antes</p>
                                                    </div>
                                                    <div className="arrow">→</div>
                                                    <div className="placeholder-box after">
                                                        <span className="icon">✨</span>
                                                        <p>Después</p>
                                                    </div>
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

                    <div className="text-center mt-5">
                        <p className="cta-text">
                            ¿Quieres que tu vehículo sea nuestro próximo caso de éxito?
                        </p>
                        <button
                            className="btn btn-primary btn-lg"
                            onClick={() => navigate("/bookappointment")}
                        >
                            Agenda tu Cita Ahora
                        </button>
                    </div>
                </div>
            </section>
        </div>
    );
};
