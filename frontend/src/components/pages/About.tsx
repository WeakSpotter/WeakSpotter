import { useEffect, useState } from "react";
import { api } from "../../services/api";
import { Job } from "../../types/scan";

export default function About() {
  interface Author {
    name: string;
    surname: string;
    username: string;
    github_username: string;
    linkedin_username: string;
  }

  const authors: Author[] = [
    {
      name: "BILLY",
      surname: "Maxime",
      username: "ozeliurs",
      github_username: "ozeliurs",
      linkedin_username: "maxime-billy",
    },
    {
      name: "MARTIN",
      surname: "Amandine",
      username: "amandinemart1",
      github_username: "amandinemart1",
      linkedin_username: "amandine-martin-aaa01020b",
    },
    {
      name: "BOUCHENGUOUR",
      surname: "Mohamed",
      username: "mbouchenguour",
      github_username: "mbouchenguour",
      linkedin_username: "mohamed-bouchenguour-973559197",
    },
    {
      name: "TRANVOUEZ",
      surname: "Evan",
      username: "EvanTranvouez",
      github_username: "EvanTranvouez",
      linkedin_username: "evantranvouez",
    },
  ];

  const [tools, setTools] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTools = async () => {
      try {
        const response = await api.getInfo();
        const allTools = [...response.data.simple, ...response.data.complex];
        const dedupedTools = Array.from(
          new Set(allTools.map((tool) => tool.name)),
        ).map((name) => allTools.find((tool) => tool.name === name)!);
        setTools(dedupedTools);
      } catch {
        setError("Failed to fetch tools information.");
      } finally {
        setLoading(false);
      }
    };

    fetchTools();
  }, []);

  if (loading) {
    return <div className="text-center py-4">Loading...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500 py-4">{error}</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">About</h1>
      <h2 className="text-2xl font-semibold mb-4">Authors</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-8">
        {authors.map((author) => (
          <div key={author.username} className="card bg-base-100 shadow-xl">
            <figure className="px-10 pt-10">
              <img
                src={`https://github.com/${author.github_username}.png`}
                alt={author.name}
                className="rounded-full w-24 h-24"
              />
            </figure>
            <div className="card-body items-center text-center">
              <h2 className="card-title">
                {author.name} {author.surname}
              </h2>
              <p>@{author.username}</p>
              <div className="card-actions">
                <a
                  href={`https://github.com/${author.github_username}`}
                  className="btn btn-primary"
                >
                  GitHub
                </a>
                <a
                  href={`https://www.linkedin.com/in/${author.linkedin_username}`}
                  className="btn btn-secondary"
                >
                  LinkedIn
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
      <h2 className="text-2xl font-semibold mb-4">Tools Used</h2>
      <div className="overflow-x-auto shadow-xl">
        <table className="table table-zebra w-full bg-base-100 rounded-lg">
          <thead>
            <tr>
              <th>Name</th>
              <th>License</th>
              <th>GPL Compatible</th>
            </tr>
          </thead>
          <tbody>
            {tools.map((tool) => (
              <tr key={tool.name}>
                <td>{tool.name}</td>
                <td>
                  <a
                    href={tool.license_url}
                    className="text-blue-500 underline"
                  >
                    {tool.license_name}
                  </a>
                </td>
                <td>
                  {tool.license_gpl_compatible ? (
                    <span className="text-green-500">✔️</span>
                  ) : (
                    <span className="text-red-500">❌</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
