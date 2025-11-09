import { useEffect, useState } from "react";

type Article = {
  id: number;
  title: string;
  summary: string;
  content: string;
  image: string | null;
  author: string;
  published_at: string;
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
                  className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden"
                >
                  {article.image && (
                    <img
                      src={article.image}
                      alt={article.title}
                      className="w-full h-48 object-cover"
                    />
                  )}
                  <div className="p-6">
                    <h3 className="text-2xl font-bold text-gray-900 mb-3 hover:text-blue-600 transition">
                      {article.title}
                    </h3>

                    {article.summary && (
                      <p className="text-gray-600 mb-4 leading-relaxed">
                        {article.summary}
                      </p>
                    )}

                    <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                      <div className="flex items-center space-x-4">
                        {article.author && (
                          <span className="flex items-center">
                            <svg
                              className="w-4 h-4 mr-1"
                              fill="currentColor"
                              viewBox="0 0 20 20"
                            >
                              <path
                                fillRule="evenodd"
                                d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                                clipRule="evenodd"
                              />
                            </svg>
                            {article.author}
                          </span>
                        )}
                        <span className="flex items-center">
                          <svg
                            className="w-4 h-4 mr-1"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                          >
                            <path
                              fillRule="evenodd"
                              d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                              clipRule="evenodd"
                            />
                          </svg>
                          {formatDate(article.published_at)}
                        </span>
                      </div>
                    </div>

                    <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition duration-200 transform hover:scale-105">
                      Ver mais
                    </button>
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
