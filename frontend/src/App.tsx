import { useEffect, useState } from "react";

type Article = {
  id: number;
  title: string;
  summary: string;
  content: string;
  image: string | null;
  author_name: string;
  published_at: string;
  comments_count: number;
};

function App() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/articles/")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Erro ao carregar notícias");
        }
        return res.json();
      })
      .then((data) => {
        setArticles(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erro ao buscar artigos:", err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "long",
      year: "numeric",
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Carregando notícias...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-red-600 text-lg mb-2">❌ {error}</p>
          <button
            onClick={() => window.location.reload()}
            className="text-blue-600 hover:underline"
          >
            Tentar novamente
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-900 to-blue-700 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold text-white mb-1">
                Jornal do Commercio
              </h1>
              <p className="text-blue-200 text-sm">
                As principais notícias do dia
              </p>
            </div>
            <div className="hidden md:flex items-center space-x-6 text-white">
              <a href="#" className="hover:text-blue-200 transition">
                Início
              </a>
              <a href="#" className="hover:text-blue-200 transition">
                Política
              </a>
              <a href="#" className="hover:text-blue-200 transition">
                Economia
              </a>
              <a href="#" className="hover:text-blue-200 transition">
                Esportes
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Feed - 2/3 width */}
          <div className="lg:col-span-2 space-y-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 border-b-2 border-blue-600 pb-2">
              Últimas Notícias
            </h2>

            {articles.length === 0 ? (
              <div className="bg-white rounded-lg shadow-md p-8 text-center">
                <p className="text-gray-500">
                  Nenhuma notícia disponível no momento.
                </p>
              </div>
            ) : (
              articles.map((article) => (
                <article
                  key={article.id}
                  className="bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden cursor-pointer group"
                  onClick={() => {
                    // Navigate to article detail page
                    console.log(`Opening article ${article.id}`);
                    // TODO: Implement navigation to article detail
                  }}
                >
                  {/* Image - Full width at top */}
                  {article.image && (
                    <div className="w-full h-64 overflow-hidden">
                      <img
                        src={article.image}
                        alt={article.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                    </div>
                  )}

                  <div className="p-6">
                    {/* Title - Merriweather font, large headline style */}
                    <h3 className="text-3xl font-bold text-gray-900 mb-4 leading-tight group-hover:text-blue-600 transition" style={{ fontFamily: 'Merriweather, serif' }}>
                      {article.title}
                    </h3>

                    {/* Summary - smaller font */}
                    {article.summary && (
                      <p className="text-base text-gray-600 mb-6 leading-relaxed">
                        {article.summary}
                      </p>
                    )}

                    {/* Author name - with spacing from summary */}
                    {article.author_name && (
                      <p className="text-sm text-gray-700 font-medium mb-6">
                        Por {article.author_name}
                      </p>
                    )}

                    {/* Actions - Comments and Bookmark side by side */}
                    <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                      <button
                        className="flex items-center space-x-2 text-gray-600 hover:text-blue-600 transition"
                        onClick={(e) => {
                          e.stopPropagation();
                          console.log(`View comments for article ${article.id}`);
                        }}
                      >
                        <svg
                          className="w-5 h-5"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                          />
                        </svg>
                        <span className="font-semibold">{article.comments_count}</span>
                      </button>

                      <button
                        className="flex items-center space-x-1 text-gray-600 hover:text-blue-600 transition"
                        onClick={(e) => {
                          e.stopPropagation();
                          console.log(`Bookmark article ${article.id}`);
                        }}
                      >
                        <svg
                          className="w-5 h-5"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
                          />
                        </svg>
                      </button>
                    </div>
                  </div>
                </article>
              ))
            )}
          </div>

          {/* Right Sidebar - 1/3 width */}
          <aside className="space-y-6">
            {/* Trending Section */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4 border-b-2 border-blue-600 pb-2">
                📈 Mais Lidas
              </h3>
              <div className="space-y-3">
                {articles.slice(0, 5).map((article, index) => (
                  <div
                    key={article.id}
                    className="flex items-start space-x-3 pb-3 border-b border-gray-100 last:border-0"
                  >
                    <span className="text-2xl font-bold text-blue-600">
                      {index + 1}
                    </span>
                    <div>
                      <h4 className="text-sm font-semibold text-gray-800 hover:text-blue-600 cursor-pointer line-clamp-2">
                        {article.title}
                      </h4>
                      <p className="text-xs text-gray-500 mt-1">
                        {formatDate(article.published_at)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Categories */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4 border-b-2 border-blue-600 pb-2">
                📂 Categorias
              </h3>
              <div className="space-y-2">
                {["Política", "Economia", "Esportes", "Cultura", "Tecnologia"].map(
                  (category) => (
                    <a
                      key={category}
                      href="#"
                      className="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 px-3 py-2 rounded transition"
                    >
                      {category}
                    </a>
                  )
                )}
              </div>
            </div>

            {/* Newsletter */}
            <div className="bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg shadow-md p-6 text-white">
              <h3 className="text-xl font-bold mb-3">📧 Newsletter</h3>
              <p className="text-sm mb-4 text-blue-100">
                Receba as principais notícias no seu e-mail
              </p>
              <input
                type="email"
                placeholder="Seu e-mail"
                className="w-full px-4 py-2 rounded-lg text-gray-800 mb-3 focus:outline-none focus:ring-2 focus:ring-blue-300"
              />
              <button className="w-full bg-white text-blue-600 font-semibold py-2 rounded-lg hover:bg-blue-50 transition">
                Inscrever-se
              </button>
            </div>
          </aside>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-12 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-gray-400">
            © 2025 Jornal do Commercio. Todos os direitos reservados.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
