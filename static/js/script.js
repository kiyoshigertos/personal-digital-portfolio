/**
 * MICHAEL ANGELO GERTOS - DIGITAL PORTFOLIO
 * Frontend Interactive Architecture & Engine
 */

document.addEventListener('DOMContentLoaded', () => {
    initHeaderAndNav();
    initTypingEffect();
    initSkillsFilter();
    initProjectModal();
    initCertificatesFilter();
    initCertificateModal();
    initContactForm();
    initBackToTop();
    initScrollReveal();
});


/* ============================================================
   1. NAVIGATION & MOBILE DRAWER
   ============================================================ */
function initHeaderAndNav() {
    const navbar = document.getElementById('navbar');
    const mobileBtn = document.getElementById('mobileMenuBtn');
    const mobileNav = document.getElementById('mobileNav');
    const mobileLinks = document.querySelectorAll('.mobile-nav-link');
    const desktopLinks = document.querySelectorAll('.desktop-nav .nav-link');

    // Header scroll background elevation
    window.addEventListener('scroll', () => {
        if (window.scrollY > 40) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        updateActiveSection(desktopLinks);
    });

    // Mobile Hamburger Toggle
    if (mobileBtn && mobileNav) {
        mobileBtn.addEventListener('click', () => {
            const isOpen = mobileNav.classList.contains('open');
            if (isOpen) {
                closeMobileNav();
            } else {
                openMobileNav();
            }
        });

        // Close on clicking any link
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                closeMobileNav();
            });
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (mobileNav.classList.contains('open') && !mobileNav.contains(e.target) && !mobileBtn.contains(e.target)) {
                closeMobileNav();
            }
        });
    }

    function openMobileNav() {
        mobileNav.classList.add('open');
        mobileBtn.classList.add('is-active');
        mobileBtn.setAttribute('aria-expanded', 'true');
        mobileNav.setAttribute('aria-hidden', 'false');
    }

    function closeMobileNav() {
        mobileNav.classList.remove('open');
        mobileBtn.classList.remove('is-active');
        mobileBtn.setAttribute('aria-expanded', 'false');
        mobileNav.setAttribute('aria-hidden', 'true');
    }
}

// Scroll spy for active navigation highlighting
function updateActiveSection(navLinks) {
    const sections = document.querySelectorAll('section[id]');
    const scrollPosition = window.scrollY + 140;

    sections.forEach(section => {
        const top = section.offsetTop;
        const height = section.offsetHeight;
        const id = section.getAttribute('id');

        if (scrollPosition >= top && scrollPosition < top + height) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href').endsWith('#' + id)) {
                    link.classList.add('active');
                }
            });
        }
    });
}

/* ============================================================
   2. DYNAMIC TYPING ANIMATION
   ============================================================ */
function initTypingEffect() {
    const typingElement = document.getElementById('typingText');
    if (!typingElement) return;

    const titles = [
        "Junior Software Developer",
        "IT Specialist",
        "Full-Stack Developer",
        "Systems & IoT Enthusiast"
    ];

    let titleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const typingSpeed = 90;
    const deletingSpeed = 45;
    const pauseDelay = 1800;

    function type() {
        const currentTitle = titles[titleIndex];

        if (isDeleting) {
            typingElement.textContent = currentTitle.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typingElement.textContent = currentTitle.substring(0, charIndex + 1);
            charIndex++;
        }

        let speed = isDeleting ? deletingSpeed : typingSpeed;

        if (!isDeleting && charIndex === currentTitle.length) {
            speed = pauseDelay;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            titleIndex = (titleIndex + 1) % titles.length;
            speed = 400;
        }

        setTimeout(type, speed);
    }

    type();
}

/* ============================================================
   3. SKILLS CATEGORY FILTER
   ============================================================ */
function initSkillsFilter() {
    const filterButtons = document.querySelectorAll('.skills-filter-nav .filter-btn');
    const skillCards = document.querySelectorAll('.skills-showcase .skill-card');

    if (!filterButtons.length || !skillCards.length) return;

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => {
                b.classList.remove('active');
                b.setAttribute('aria-selected', 'false');
            });
            btn.classList.add('active');
            btn.setAttribute('aria-selected', 'true');

            const category = btn.getAttribute('data-category');

            skillCards.forEach(card => {
                const domain = card.getAttribute('data-domain');
                if (category === 'all' || domain === category) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

/* ============================================================
   4. INTERACTIVE PROJECT MODAL QUICK-VIEW
   ============================================================ */
function initProjectModal() {
    const modal = document.getElementById('projectModal');
    const modalContent = document.getElementById('modalContent');
    const closeBtn = document.getElementById('modalCloseBtn');
    const backdrop = document.getElementById('modalBackdrop');
    const openButtons = document.querySelectorAll('.open-modal-btn');

    if (!modal || !modalContent) return;

    openButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const slug = btn.getAttribute('data-slug');
            openModal(slug);
        });
    });

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (backdrop) backdrop.addEventListener('click', closeModal);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });

    async function openModal(slug) {
        modal.classList.add('active');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';

        modalContent.innerHTML = `
            <div class="modal-loading">
                <div class="spinner"></div>
                <p>Loading project details...</p>
            </div>
        `;

        try {
            const response = await fetch(`/api/project/${slug}`);
            const data = await response.json();

            if (data.status === 'success' && data.project) {
                renderModalContent(data.project);
            } else {
                modalContent.innerHTML = `<p class="text-center text-muted">Unable to load project information.</p>`;
            }
        } catch (err) {
            modalContent.innerHTML = `<p class="text-center text-muted">Network error loading project details.</p>`;
        }
    }

    function renderModalContent(p) {
        let clientsHtml = '';
        if (p.clients && p.clients.length > 0) {
            const clientTags = p.clients.map(c => `<span class="client-tag">${c.name}</span>`).join('');
            clientsHtml = `
                <div class="project-clients-box" style="margin-top: 14px;">
                    <span class="clients-label">Deployed for Clients:</span>
                    <div class="client-tags">${clientTags}</div>
                </div>
            `;
        }

        let featuresHtml = '';
        if (p.feature_breakdown) {
            featuresHtml = `
                <div style="margin-top: 16px;">
                    <h4 style="font-size: 0.95rem; margin-bottom: 8px; color: var(--text-primary);">Feature Architecture:</h4>
                    <p style="font-size: 0.85rem; color: #10b981;"><strong>Implemented:</strong> ${p.feature_breakdown.implemented.join(' • ')}</p>
                    <p style="font-size: 0.85rem; color: #38bdf8; margin-top: 4px;"><strong>Planned:</strong> ${p.feature_breakdown.planned.join(' • ')}</p>
                </div>
            `;
        } else if (p.key_features) {
            const list = p.key_features.map(f => `<li style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 4px;">✓ ${f}</li>`).join('');
            featuresHtml = `
                <div style="margin-top: 16px;">
                    <h4 style="font-size: 0.95rem; margin-bottom: 8px; color: var(--text-primary);">Key Features:</h4>
                    <ul>${list}</ul>
                </div>
            `;
        }

        const techPills = p.technologies.map(t => `<span class="tech-pill">${t}</span>`).join('');

        modalContent.innerHTML = `
            <div class="modal-project-header">
                <div class="project-meta-row" style="margin-bottom: 6px;">
                    <span class="project-category">${p.category}</span>
                    <span class="project-status">${p.status}</span>
                </div>
                <h2 style="font-family: var(--font-heading); font-size: 1.8rem; color: var(--text-primary); margin-bottom: 4px;">${p.title}</h2>
                <p style="font-size: 0.95rem; color: var(--accent-primary); margin-bottom: 14px;">${p.type}</p>
                
                ${p.tagline ? `<p style="font-style: italic; color: #c084fc; margin-bottom: 12px;">"${p.tagline}"</p>` : ''}
            </div>

            <div class="modal-project-body">
                <p style="font-size: 0.95rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 14px;">
                    ${p.short_description}
                </p>

                <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 14px; margin-bottom: 14px;">
                    <strong style="color: var(--accent-primary); font-size: 0.85rem; display: block; margin-bottom: 4px;">Engineering Role:</strong>
                    <span style="font-size: 0.88rem; color: var(--text-primary);">${p.my_role}</span>
                </div>

                ${clientsHtml}
                ${featuresHtml}

                <div style="margin-top: 20px;">
                    <span style="display: block; font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 8px;">Stack &amp; Technologies</span>
                    <div class="project-tech-stack" style="margin-bottom: 0;">${techPills}</div>
                </div>

                <div style="margin-top: 24px; padding-top: 18px; border-top: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <a href="/project/${p.slug}" class="btn btn-primary btn-sm">
                        <span>View Full Case Study</span>
                        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                    </a>
                    <button class="btn btn-outline btn-sm" onclick="document.getElementById('modalCloseBtn').click()">Close Preview</button>
                </div>
            </div>
        `;
    }

    function closeModal() {
        modal.classList.remove('active');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }
}

/* ============================================================
   4B. CERTIFICATES & CREDENTIALS FILTER
   ============================================================ */
function initCertificatesFilter() {
    const filterButtons = document.querySelectorAll('.cert-filter-btn');
    const certCards = document.querySelectorAll('.cert-showcase-card');

    if (!filterButtons.length || !certCards.length) return;

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const filter = btn.getAttribute('data-filter');

            // Update active states
            filterButtons.forEach(b => {
                b.classList.remove('active');
                b.setAttribute('aria-selected', 'false');
            });
            btn.classList.add('active');
            btn.setAttribute('aria-selected', 'true');

            // Filter cards with smooth opacity
            certCards.forEach(card => {
                const cardType = card.getAttribute('data-credential-type');
                const shouldShow = (filter === 'all' || cardType === filter);

                if (shouldShow) {
                    card.style.display = 'flex';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 20);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(10px)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 250);
                }
            });
        });
    });
}

/* ============================================================
   4C. CERTIFICATE LIGHTBOX / MODAL VIEWER
   ============================================================ */
function initCertificateModal() {
    const modal = document.getElementById('certModal');
    const modalContent = document.getElementById('certModalContent');
    const closeBtn = document.getElementById('certModalCloseBtn');
    const backdrop = document.getElementById('certModalBackdrop');
    const openButtons = document.querySelectorAll('.open-cert-modal-btn');

    if (!modal || !modalContent) return;

    // Attach click listeners to all certificate open buttons
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.open-cert-modal-btn');
        if (btn) {
            e.preventDefault();
            const certId = btn.getAttribute('data-cert-id');
            if (certId) openCertModal(certId);
        }
    });

    if (closeBtn) closeBtn.addEventListener('click', closeCertModal);
    if (backdrop) backdrop.addEventListener('click', closeCertModal);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeCertModal();
        }
    });

    async function openCertModal(certId) {
        modal.classList.add('active');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';

        modalContent.innerHTML = `
            <div class="modal-loading">
                <div class="spinner"></div>
                <p>Loading certificate credentials...</p>
            </div>
        `;

        try {
            const response = await fetch(`/api/certifications/${certId}`);
            const data = await response.json();

            if (data.status === 'success' && data.certification) {
                renderCertModalContent(data.certification);
            } else {
                modalContent.innerHTML = `<p class="text-center text-muted">Unable to load certificate information.</p>`;
            }
        } catch (err) {
            modalContent.innerHTML = `<p class="text-center text-muted">Network error loading certificate details.</p>`;
        }
    }

    function renderCertModalContent(c) {
        const imgSrc = c.image ? `/static/images/${c.image}` : null;
        
        let compsHtml = '';
        if (c.skills_covered && c.skills_covered.length > 0) {
            const items = c.skills_covered.map(s => `<li>${s}</li>`).join('');
            compsHtml = `
                <div style="margin-top: 16px;">
                    <h4 class="cert-lightbox-comp-title">Verified Units &amp; Competencies:</h4>
                    <ul class="cert-lightbox-comp-list">${items}</ul>
                </div>
            `;
        }

        let idNumberHtml = '';
        if (c.cert_no) {
            idNumberHtml = `
                <div class="cert-info-item">
                    <span class="cert-info-label">Certificate ID / No.</span>
                    <span class="cert-info-value">${c.cert_no}</span>
                </div>
            `;
        } else if (c.gwa) {
            idNumberHtml = `
                <div class="cert-info-item">
                    <span class="cert-info-label">Academic Distinction</span>
                    <span class="cert-info-value" style="color: #fbbf24;">${c.gwa}</span>
                </div>
            `;
        }

        let validityHtml = '';
        if (c.validity) {
            validityHtml = `
                <div class="cert-info-item">
                    <span class="cert-info-label">Validity Status</span>
                    <span class="cert-info-value" style="color: #10b981;">${c.validity}</span>
                </div>
            `;
        } else if (c.issued_date) {
            validityHtml = `
                <div class="cert-info-item">
                    <span class="cert-info-label">Date Issued</span>
                    <span class="cert-info-value">${c.issued_date}</span>
                </div>
            `;
        }

        let signatoriesHtml = '';
        if (c.signatory) {
            signatoriesHtml = `
                <div class="cert-lightbox-signatories">
                    <strong>Official Signatory / Verification:</strong><br>
                    <span>${c.signatory}</span>
                </div>
            `;
        }

        const imagePanelHtml = imgSrc ? `
            <div class="cert-lightbox-image-panel">
                <img src="${imgSrc}" alt="${c.title}" class="cert-lightbox-img" id="lightboxCertImg" title="Click to zoom">
                <div class="cert-lightbox-actions">
                    <span style="font-size: 0.75rem; color: var(--text-muted);">💡 Click photo to zoom in/out</span>
                    <a href="${imgSrc}" target="_blank" rel="noopener noreferrer" class="btn btn-outline btn-sm">
                        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                        <span>Open High-Res Scan</span>
                    </a>
                </div>
            </div>
        ` : `
            <div class="cert-lightbox-image-panel" style="display:flex; align-items:center; justify-content:center; min-height: 250px;">
                <div style="text-align: center;">
                    <div style="font-size: 3.5rem; margin-bottom: 8px;">📜</div>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">Official Institutional Credential</p>
                </div>
            </div>
        `;

        modalContent.innerHTML = `
            <div class="cert-lightbox-layout">
                ${imagePanelHtml}

                <div class="cert-lightbox-details-panel">
                    <span class="cert-lightbox-meta-badge">${c.badge}</span>
                    <h2 class="cert-lightbox-title">${c.title}</h2>
                    <p class="cert-lightbox-issuer">${c.issuer}</p>

                    <div class="cert-lightbox-info-grid">
                        <div class="cert-info-item">
                            <span class="cert-info-label">Credential Type</span>
                            <span class="cert-info-value">${c.category_label}</span>
                        </div>
                        <div class="cert-info-item">
                            <span class="cert-info-label">Issued / Conferred</span>
                            <span class="cert-info-value">${c.issued_date || c.year}</span>
                        </div>
                        ${idNumberHtml}
                        ${validityHtml}
                    </div>

                    ${signatoriesHtml}

                    <p style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.55; margin-bottom: 12px;">
                        ${c.highlight}
                    </p>

                    ${compsHtml}

                    <div style="margin-top: auto; padding-top: 16px; border-top: 1px solid var(--border-subtle); display: flex; justify-content: flex-end; gap: 10px;">
                        <button class="btn btn-primary btn-sm" onclick="document.getElementById('certModalCloseBtn').click()">
                            <span>Close Viewer</span>
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Attach zoom handler
        const img = document.getElementById('lightboxCertImg');
        if (img) {
            img.addEventListener('click', () => {
                img.classList.toggle('zoomed');
            });
        }
    }

    function closeCertModal() {
        modal.classList.remove('active');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }
}

function initContactForm() {
    const form = document.getElementById('contactForm');
    const submitBtn = document.getElementById('contactSubmitBtn');
    if (!form || !submitBtn) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const nameInput = document.getElementById('contactName');
        const emailInput = document.getElementById('contactEmail');
        const subjectInput = document.getElementById('contactSubject');
        const messageInput = document.getElementById('contactMessage');

        let isValid = true;

        // Reset errors
        [nameInput, emailInput, messageInput].forEach(input => {
            input.classList.remove('is-invalid');
        });

        // Validation
        if (!nameInput.value.trim()) {
            nameInput.classList.add('is-invalid');
            document.getElementById('nameError').textContent = 'Please enter your name.';
            isValid = false;
        }

        const emailVal = emailInput.value.trim();
        if (!emailVal || !emailVal.includes('@') || !emailVal.includes('.')) {
            emailInput.classList.add('is-invalid');
            document.getElementById('emailError').textContent = 'Please enter a valid email address.';
            isValid = false;
        }

        if (!messageInput.value.trim()) {
            messageInput.classList.add('is-invalid');
            document.getElementById('messageError').textContent = 'Please write a message.';
            isValid = false;
        }

        if (!isValid) return;

        // Button Loading State
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
            <div class="spinner" style="width: 18px; height: 18px; margin: 0; border-width: 2px;"></div>
            <span>Recording Message...</span>
        `;

        try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    name: nameInput.value.trim(),
                    email: emailInput.value.trim(),
                    subject: subjectInput.value.trim(),
                    message: messageInput.value.trim()
                })
            });

            const result = await response.json();

            if (response.ok && result.status === 'success') {
                showToast(result.message || 'Thank you! Your message has been received.', false);
                form.reset();
            } else {
                showToast(result.message || 'Error sending message. Please try again.', true);
            }
        } catch (error) {
            showToast('Unable to connect to the server. Please check your connection.', true);
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}

// Toast notification helper
function showToast(message, isError = false) {
    const toast = document.getElementById('toastNotification');
    const toastMessage = document.getElementById('toastMessage');
    const toastIcon = document.getElementById('toastIcon');

    if (!toast || !toastMessage) return;

    toastMessage.textContent = message;
    if (isError) {
        toast.classList.add('toast-error');
        toastIcon.innerHTML = '⚠️';
    } else {
        toast.classList.remove('toast-error');
        toastIcon.innerHTML = '✓';
    }

    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 5000);
}

/* ============================================================
   7. SCROLL REVEAL (IntersectionObserver)
   ============================================================ */
function initScrollReveal() {
    const elements = document.querySelectorAll('.reveal-on-scroll');
    if (!elements.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px'
    });

    elements.forEach(el => observer.observe(el));
}

/* ============================================================
   6. BACK TO TOP BUTTON
   ============================================================ */
function initBackToTop() {
    const backToTopBtn = document.getElementById('backToTopBtn');
    if (!backToTopBtn) return;

    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}
