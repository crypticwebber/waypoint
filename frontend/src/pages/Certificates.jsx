import { useCallback, useState } from "react";
import { Link } from "react-router-dom";
import { Download, Award, GraduationCap } from "lucide-react";
import { certificatesApi } from "../api/resources";
import { useFetch } from "../hooks/useFetch";
import { useToast } from "../context/ToastContext";
import { extractErrorMessage } from "../api/client";
import { CardGridSkeleton, EmptyState, ErrorState } from "../components/States";

export default function Certificates() {
  const certsFetch = useFetch(useCallback(() => certificatesApi.mine(), []));
  const { push } = useToast();
  const [downloadingId, setDownloadingId] = useState(null);

  async function handleDownload(cert) {
    setDownloadingId(cert.id);
    try {
      await certificatesApi.downloadPdf(cert.id, `waypoint-${cert.certificate_code}.pdf`);
    } catch (err) {
      push(extractErrorMessage(err), "error");
    } finally {
      setDownloadingId(null);
    }
  }

  return (
    <div className="max-w-5xl mx-auto px-5 py-10">
      <h1 className="text-2xl font-display font-semibold mb-1">Your certificates</h1>
      <p className="text-mist mb-8">Earned by finishing every lesson and passing every module quiz.</p>

      {certsFetch.isLoading ? (
        <CardGridSkeleton count={3} />
      ) : certsFetch.error ? (
        <ErrorState description={certsFetch.error} onRetry={certsFetch.refetch} />
      ) : certsFetch.data.length === 0 ? (
        <EmptyState
          icon={GraduationCap}
          title="No certificates yet"
          description="Finish a course -- every lesson complete, every module quiz passed -- and your certificate appears here automatically."
          action={<Link to="/catalog" className="btn-primary">Browse courses</Link>}
        />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {certsFetch.data.map((cert) => (
            <div key={cert.id} className="card p-5 flex flex-col">
              <div className="w-11 h-11 rounded-xl bg-amber/15 flex items-center justify-center mb-4">
                <Award size={20} className="text-amber" />
              </div>
              <h3 className="font-display font-semibold mb-1.5 leading-snug">{cert.course_title}</h3>
              <p className="text-xs text-mist mb-1">Issued {new Date(cert.issued_at).toLocaleDateString()}</p>
              <p className="text-xs font-mono text-mist mb-5">{cert.certificate_code}</p>
              <button
                onClick={() => handleDownload(cert)}
                disabled={downloadingId === cert.id}
                className="btn-secondary text-sm mt-auto"
              >
                <Download size={15} /> {downloadingId === cert.id ? "Preparing…" : "Download PDF"}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
