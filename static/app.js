// Dashboard: load the admin feedback widget.
// The widget calls the admin API. The page itself does NOT send the admin
// key, so this request comes back 401 Unauthorized. Open the Console and the
// Network tab to see it.
(function () {
  var box = document.getElementById("admin-widget");
  if (!box) return;

  fetch("/api/admin/feedback")
    .then(function (r) {
      if (!r.ok) {
        throw new Error("admin API returned " + r.status);
      }
      return r.json();
    })
    .then(function (data) {
      box.textContent = JSON.stringify(data, null, 2);
    })
    .catch(function (err) {
      box.textContent = "Admin feed unavailable (you are not authorised here).";
      console.error("Admin feed failed:", err.message);
    });
})();
