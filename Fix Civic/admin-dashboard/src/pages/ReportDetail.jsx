import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getReport, updateReport, postToX, resolveReport, declineReport, getFullImageUrl } from '../api/client.js';

export default function ReportDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [adminNote, setAdminNote] = useState('');
    const [actionLoading, setActionLoading] = useState('');
    const [message, setMessage] = useState(null);

    // Resolve workflow state
    const [resolveImage, setResolveImage] = useState(null);
    const [resolveImagePreview, setResolveImagePreview] = useState(null);
    const [resolvedNote, setResolvedNote] = useState('');
    const fileInputRef = useRef(null);

    // Decline workflow state
    const [showDeclineDialog, setShowDeclineDialog] = useState(false);
    const [declineReason, setDeclineReason] = useState('Fake report');

    const DECLINE_REASONS = [
        'Fake report',
        'Duplicate report',
        'Invalid evidence',
        'Not a civic issue',
        'Insufficient information',
        'Other',
    ];

    useEffect(() => {
        fetchReport();
    }, [id]);

    const fetchReport = async () => {
        try {
            const data = await getReport(id);
            setReport(data);
            setAdminNote(data.admin_note || '');
        } catch (err) {
            console.error('Failed to fetch report:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateStatus = async (status) => {
        setActionLoading(status);
        setMessage(null);
        try {
            const updated = await updateReport(id, { status, admin_note: adminNote || undefined });
            setReport(updated);
            setMessage({ type: 'success', text: `Report marked as ${status}` });
        } catch (err) {
            setMessage({ type: 'error', text: err.response?.data?.detail || 'Update failed' });
        } finally {
            setActionLoading('');
        }
    };

    const handlePostToX = async () => {
        setActionLoading('x');
        setMessage(null);
        try {
            const result = await postToX(id);
            setMessage({ type: 'success', text: result.message });
            await fetchReport();
        } catch (err) {
            setMessage({ type: 'error', text: err.response?.data?.detail || 'Post to X failed' });
        } finally {
            setActionLoading('');
        }
    };

    // --- Resolve Workflow ---
    const handleImageSelect = (e) => {
        const file = e.target.files[0];
        if (file) {
            setResolveImage(file);
            setResolveImagePreview(URL.createObjectURL(file));
        }
    };

    const handleResolve = async () => {
        if (!resolveImage) {
            setMessage({ type: 'error', text: 'Please upload a resolution photo before resolving.' });
            return;
        }
        setActionLoading('resolving');
        setMessage(null);
        try {
            const formData = new FormData();
            formData.append('image', resolveImage);
            if (resolvedNote) {
                formData.append('resolved_note', resolvedNote);
            }
            const result = await resolveReport(id, formData);
            setReport(result.report);
            setMessage({ type: 'success', text: '✅ Report resolved successfully!' });

            // Reset resolve form
            setResolveImage(null);
            setResolveImagePreview(null);
            setResolvedNote('');

            // Open X/Twitter composer with the resolved tweet
            if (result.resolved_tweet) {
                const tweetUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(result.resolved_tweet)}`;
                window.open(tweetUrl, '_blank', 'noopener,noreferrer,width=600,height=400');
            }
        } catch (err) {
            setMessage({ type: 'error', text: err.response?.data?.detail || 'Resolve failed' });
        } finally {
            setActionLoading('');
        }
    };

    // --- Decline Workflow ---
    const handleDecline = async () => {
        setShowDeclineDialog(false);
        setActionLoading('declining');
        setMessage(null);
        try {
            const result = await declineReport(id, declineReason);
            setReport(result.report);
            setMessage({ type: 'success', text: '❌ Report declined and marked as fake.' });
            setDeclineReason('Fake report');

            // Open X/Twitter composer with the declined tweet
            if (result.declined_tweet) {
                const tweetUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(result.declined_tweet)}`;
                window.open(tweetUrl, '_blank', 'noopener,noreferrer,width=600,height=400');
            }
        } catch (err) {
            setMessage({ type: 'error', text: err.response?.data?.detail || 'Decline failed' });
        } finally {
            setActionLoading('');
        }
    };

    if (loading) {
        return <div className="loading"><div className="spinner"></div>Loading report...</div>;
    }

    if (!report) {
        return (
            <div className="empty-state">
                <span className="material-icons-outlined">error_outline</span>
                <p>Report not found</p>
            </div>
        );
    }

    const mapsUrl = `https://maps.google.com/?q=${report.latitude},${report.longitude}`;
    const isResolved = report.status === 'resolved';
    const isDeclined = report.status === 'declined';
    const isFinal = isResolved || isDeclined;

    return (
        <>
            <a className="back-link" onClick={() => navigate(-1)}>
                <span className="material-icons-outlined" style={{ fontSize: 18 }}>arrow_back</span>
                Back to reports
            </a>

            <div className="page-header">
                <h2>Report Detail</h2>
                <p>Report ID: {report.id}</p>
            </div>

            {message && (
                <div className={`error-msg`} style={{
                    background: message.type === 'success' ? '#ecfdf5' : undefined,
                    color: message.type === 'success' ? '#047857' : undefined,
                    marginBottom: 20,
                }}>
                    {message.text}
                </div>
            )}

            <div className="detail-grid">
                {/* Left: Image & Map */}
                <div>
                    <div className="card" style={{ marginBottom: 20 }}>
                        <div className="card-header">
                            <h3>📸 Evidence Photo</h3>
                            {report.is_fake && (
                                <span style={{
                                    background: '#fef2f2', color: '#dc2626', padding: '4px 10px',
                                    borderRadius: 6, fontSize: 12, fontWeight: 700
                                }}>
                                    ⚠️ FAKE
                                </span>
                            )}
                        </div>
                        <div className="detail-image">
                            {report.image_url ? (
                                <img src={getFullImageUrl(report.image_url)} alt="Report evidence" />
                            ) : (
                                <div style={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f1f5f9' }}>
                                    <span className="material-icons-outlined" style={{ fontSize: 48, color: '#cbd5e1' }}>image</span>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Resolution Photo (shown after resolve) */}
                    {report.resolved_image_url && (
                        <div className="card" style={{ marginBottom: 20 }}>
                            <div className="card-header">
                                <h3>✅ Resolution Photo</h3>
                            </div>
                            <div className="detail-image">
                                <img src={getFullImageUrl(report.resolved_image_url)} alt="Resolution evidence" />
                            </div>
                            <div className="card-body">
                                {report.resolved_at && (
                                    <div className="detail-field">
                                        <div className="label">Resolved At</div>
                                        <div className="value">{new Date(report.resolved_at).toLocaleString()}</div>
                                    </div>
                                )}
                                {report.resolved_by && (
                                    <div className="detail-field">
                                        <div className="label">Resolved By</div>
                                        <div className="value">{report.resolved_by}</div>
                                    </div>
                                )}
                                {report.resolved_note && (
                                    <div className="detail-field">
                                        <div className="label">Resolution Note</div>
                                        <div className="value">{report.resolved_note}</div>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Decline Info (shown after decline) */}
                    {isDeclined && (
                        <div className="card" style={{ marginBottom: 20, border: '2px solid #ef4444' }}>
                            <div className="card-header" style={{ background: '#fef2f2' }}>
                                <h3>❌ Report Declined</h3>
                                <span style={{
                                    background: '#dc2626', color: 'white', padding: '4px 10px',
                                    borderRadius: 6, fontSize: 12, fontWeight: 700
                                }}>
                                    FAKE / INVALID
                                </span>
                            </div>
                            <div className="card-body">
                                {report.decline_reason && (
                                    <div className="detail-field">
                                        <div className="label">Decline Reason</div>
                                        <div className="value" style={{ color: '#dc2626', fontWeight: 600 }}>{report.decline_reason}</div>
                                    </div>
                                )}
                                {report.declined_at && (
                                    <div className="detail-field">
                                        <div className="label">Declined At</div>
                                        <div className="value">{new Date(report.declined_at).toLocaleString()}</div>
                                    </div>
                                )}
                                {report.declined_by && (
                                    <div className="detail-field">
                                        <div className="label">Declined By</div>
                                        <div className="value">{report.declined_by}</div>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    <div className="card">
                        <div className="card-header">
                            <h3>📍 Location</h3>
                            <a href={mapsUrl} target="_blank" rel="noopener noreferrer" className="btn btn-outline btn-sm">
                                <span className="material-icons-outlined" style={{ fontSize: 16 }}>open_in_new</span>
                                Google Maps
                            </a>
                        </div>
                        <div className="card-body">
                            <div className="detail-field">
                                <div className="label">Address</div>
                                <div className="value">{report.address || 'Not available'}</div>
                            </div>
                            <div className="detail-field">
                                <div className="label">Coordinates</div>
                                <div className="value">{report.latitude.toFixed(6)}, {report.longitude.toFixed(6)}</div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right: Details */}
                <div>
                    <div className="card" style={{ marginBottom: 20 }}>
                        <div className="card-header">
                            <h3>Report Information</h3>
                            <span className={`badge ${report.status}`} style={
                                isDeclined ? { background: '#fef2f2', color: '#dc2626' } : undefined
                            }>
                                {isDeclined ? '❌ declined' : report.status}
                            </span>
                        </div>
                        <div className="card-body">
                            <div className="detail-field">
                                <div className="label">Issue Type</div>
                                <div className="value" style={{ fontSize: 18, fontWeight: 600 }}>{report.issue_type}</div>
                            </div>
                            <div className="detail-field">
                                <div className="label">Description</div>
                                <div className="value">{report.description}</div>
                            </div>
                            <div className="detail-field">
                                <div className="label">Submitted</div>
                                <div className="value">
                                    {new Date(report.created_at).toLocaleString('en-US', {
                                        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
                                        hour: '2-digit', minute: '2-digit'
                                    })}
                                </div>
                            </div>
                            <div className="detail-field">
                                <div className="label">Posted to X</div>
                                <div className="value">
                                    {report.posted_to_x ? (
                                        <span style={{ color: '#10b981' }}>✅ Posted (ID: {report.x_post_id})</span>
                                    ) : (
                                        <span style={{ color: '#94a3b8' }}>Not posted</span>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Complaint Text */}
                    {report.complaint_text && (
                        <div className="card" style={{ marginBottom: 20 }}>
                            <div className="card-header">
                                <h3>📄 Complaint Text</h3>
                            </div>
                            <div className="card-body">
                                <div className="complaint-box">{report.complaint_text}</div>
                            </div>
                        </div>
                    )}

                    {/* Admin Actions */}
                    <div className="card" style={{ marginBottom: 20 }}>
                        <div className="card-header">
                            <h3>🛠️ Admin Actions</h3>
                        </div>
                        <div className="card-body">
                            <div className="form-group">
                                <label htmlFor="admin-note">Admin Note</label>
                                <textarea
                                    id="admin-note"
                                    value={adminNote}
                                    onChange={(e) => setAdminNote(e.target.value)}
                                    placeholder="Add a note about this report..."
                                    rows={3}
                                />
                            </div>

                            <div className="action-bar" style={{ marginTop: 0, paddingTop: 0, borderTop: 'none' }}>
                                <button
                                    className="btn btn-primary btn-sm"
                                    onClick={() => handleUpdateStatus('approved')}
                                    disabled={!!actionLoading || report.status === 'approved'}
                                >
                                    {actionLoading === 'approved' ? '...' : '👍 Approve'}
                                </button>
                                <button
                                    className="btn btn-danger btn-sm"
                                    onClick={() => handleUpdateStatus('rejected')}
                                    disabled={!!actionLoading || report.status === 'rejected'}
                                >
                                    {actionLoading === 'rejected' ? '...' : '❌ Reject'}
                                </button>
                                <button
                                    className="btn btn-outline btn-sm"
                                    onClick={handlePostToX}
                                    disabled={!!actionLoading || report.posted_to_x}
                                >
                                    {actionLoading === 'x' ? '...' : '🐦 Post to X'}
                                </button>
                            </div>
                        </div>
                    </div>

                    {/* Resolve & Decline Section — only shown if not in a final state */}
                    {!isFinal && (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                            {/* Resolve Section */}
                            <div className="card" style={{
                                border: '2px solid #10b981',
                                background: 'linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%)',
                            }}>
                                <div className="card-header">
                                    <h3>✅ Resolve Report</h3>
                                </div>
                                <div className="card-body">
                                    <p style={{ color: '#047857', marginBottom: 16, fontSize: 14 }}>
                                        Upload a photo of the resolved issue, then click "Mark Resolved" to complete the workflow.
                                    </p>

                                    {/* Image Upload */}
                                    <div className="form-group">
                                        <label>Resolution Photo <span style={{ color: '#ef4444' }}>*</span></label>
                                        <input
                                            type="file"
                                            ref={fileInputRef}
                                            accept="image/jpeg,image/png"
                                            onChange={handleImageSelect}
                                            style={{ display: 'none' }}
                                        />
                                        <button
                                            className="btn btn-outline"
                                            onClick={() => fileInputRef.current?.click()}
                                            style={{ width: '100%', padding: '12px', marginBottom: 12 }}
                                        >
                                            <span className="material-icons-outlined" style={{ fontSize: 20, verticalAlign: 'middle', marginRight: 8 }}>upload</span>
                                            {resolveImage ? 'Change Photo' : 'Upload Resolution Photo'}
                                        </button>

                                        {/* Image Preview */}
                                        {resolveImagePreview && (
                                            <div style={{
                                                borderRadius: 8, overflow: 'hidden', marginBottom: 12,
                                                border: '2px solid #10b981', position: 'relative'
                                            }}>
                                                <img
                                                    src={resolveImagePreview}
                                                    alt="Resolution preview"
                                                    style={{ width: '100%', maxHeight: 250, objectFit: 'cover' }}
                                                />
                                                <div style={{
                                                    position: 'absolute', top: 8, right: 8,
                                                    background: '#10b981', color: 'white', borderRadius: 4,
                                                    padding: '2px 8px', fontSize: 12, fontWeight: 600
                                                }}>
                                                    ✓ Ready
                                                </div>
                                            </div>
                                        )}
                                    </div>

                                    {/* Resolution Note */}
                                    <div className="form-group">
                                        <label>Resolution Note (optional)</label>
                                        <textarea
                                            value={resolvedNote}
                                            onChange={(e) => setResolvedNote(e.target.value)}
                                            placeholder="Describe how the issue was resolved..."
                                            rows={2}
                                        />
                                    </div>

                                    {/* Resolve Button */}
                                    <button
                                        className="btn btn-success"
                                        onClick={handleResolve}
                                        disabled={!!actionLoading || !resolveImage}
                                        style={{ width: '100%', padding: '12px', fontSize: 16, fontWeight: 600 }}
                                    >
                                        {actionLoading === 'resolving' ? (
                                            <>⏳ Resolving...</>
                                        ) : (
                                            <>✅ Mark Resolved & Open Tweet Composer</>
                                        )}
                                    </button>
                                </div>
                            </div>

                            {/* Decline Section */}
                            <div className="card" style={{
                                border: '2px solid #ef4444',
                                background: 'linear-gradient(135deg, #fef2f2 0%, #fff1f2 100%)',
                            }}>
                                <div className="card-header">
                                    <h3>❌ Decline Report</h3>
                                </div>
                                <div className="card-body">
                                    <p style={{ color: '#991b1b', marginBottom: 16, fontSize: 14 }}>
                                        Mark this report as fake or invalid. A tweet will be generated to inform the community.
                                    </p>

                                    <button
                                        className="btn btn-danger"
                                        onClick={() => setShowDeclineDialog(true)}
                                        disabled={!!actionLoading}
                                        style={{ width: '100%', padding: '12px', fontSize: 16, fontWeight: 600 }}
                                    >
                                        {actionLoading === 'declining' ? (
                                            <>⏳ Declining...</>
                                        ) : (
                                            <>🚫 Decline & Mark as Fake</>
                                        )}
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Decline Confirmation Dialog */}
            {showDeclineDialog && (
                <div style={{
                    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                    background: 'rgba(0,0,0,0.5)', display: 'flex',
                    alignItems: 'center', justifyContent: 'center', zIndex: 1000
                }}>
                    <div style={{
                        background: 'white', borderRadius: 16, padding: 24,
                        maxWidth: 460, width: '90%', boxShadow: '0 20px 60px rgba(0,0,0,0.3)'
                    }}>
                        <h3 style={{ margin: '0 0 8px', fontSize: 20, color: '#dc2626' }}>
                            🚫 Decline Report
                        </h3>
                        <p style={{ margin: '0 0 20px', color: '#64748b', fontSize: 14 }}>
                            This will mark the report as fake/invalid. A tweet will be generated for you to post.
                        </p>

                        <div style={{ marginBottom: 16 }}>
                            <label style={{ display: 'block', marginBottom: 6, fontWeight: 600, fontSize: 14 }}>
                                Decline Reason
                            </label>
                            <select
                                value={declineReason}
                                onChange={(e) => setDeclineReason(e.target.value)}
                                style={{
                                    width: '100%', padding: '10px 12px', borderRadius: 8,
                                    border: '1px solid #e2e8f0', fontSize: 14, outline: 'none'
                                }}
                            >
                                {DECLINE_REASONS.map(r => (
                                    <option key={r} value={r}>{r}</option>
                                ))}
                            </select>
                        </div>

                        <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
                            <button
                                className="btn btn-outline btn-sm"
                                onClick={() => setShowDeclineDialog(false)}
                            >
                                Cancel
                            </button>
                            <button
                                className="btn btn-danger btn-sm"
                                onClick={handleDecline}
                            >
                                ❌ Confirm Decline
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}
