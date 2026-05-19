const header = document.querySelector("[data-header]");
const year = document.querySelector("[data-year]");
const navLinks = [...document.querySelectorAll(".site-nav a")];
const sections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

if (year) {
  year.textContent = new Date().getFullYear();
}

const updateHeader = () => {
  header?.classList.toggle("is-scrolled", window.scrollY > 10);
};

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { rootMargin: "0px 0px -10% 0px", threshold: 0.12 }
);

document.querySelectorAll(".reveal").forEach((element) => {
  revealObserver.observe(element);
});

const activeObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      navLinks.forEach((link) => {
        link.classList.toggle("is-active", link.getAttribute("href") === `#${entry.target.id}`);
      });
    });
  },
  { rootMargin: "-35% 0px -55% 0px", threshold: 0 }
);

sections.forEach((section) => activeObserver.observe(section));
window.addEventListener("scroll", updateHeader, { passive: true });
updateHeader();

const formatCitationCount = (count) => `${Number(count).toLocaleString()} citation${count === 1 ? "" : "s"}`;

const setCitationBadge = (paper, text, state, sourceTitle) => {
  const badge = paper.querySelector("[data-citation-badge]");
  if (!badge) return;
  badge.textContent = text;
  badge.classList.remove("is-loading", "is-loaded", "is-missing", "is-error");
  badge.classList.add(state);
  badge.title = sourceTitle || "Citation count from Google Scholar";
};

const getCitationData = async () => {
  if (window.__CITATION_DATA__) {
    return window.__CITATION_DATA__;
  }

  const response = await fetch("_data/citations.json", { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Citation data responded with ${response.status}`);
  }

  return response.json();
};

const loadCitationBadges = async () => {
  const papers = [...document.querySelectorAll(".paper-item[data-citation-key]")];
  if (!papers.length) return;

  try {
    const citationData = await getCitationData();
    const lastUpdated = citationData.last_updated ? ` Last updated ${citationData.last_updated}.` : "";

    papers.forEach((paper) => {
      const citation = citationData.papers?.[paper.dataset.citationKey];
      const hasCitationCount = citation?.citations !== null && citation?.citations !== undefined;
      const count = Number(citation?.citations);

      if (hasCitationCount && Number.isFinite(count)) {
        setCitationBadge(
          paper,
          formatCitationCount(count),
          "is-loaded",
          `Google Scholar citation count for "${citation.title}".${lastUpdated}`
        );
      } else {
        setCitationBadge(paper, "Citations pending", "is-missing", "Not found in Google Scholar data yet");
      }
    });
  } catch (error) {
    papers.forEach((paper) => {
      if (paper.querySelector(".citation-badge.is-loading")) {
        setCitationBadge(paper, "Citations unavailable", "is-error", "Could not load local citation data");
      }
    });
  }
};

loadCitationBadges();
