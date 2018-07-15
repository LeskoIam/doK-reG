SELECT
  *
FROM
  revision r
JOIN document d ON r.document_id = d.id
JOIN project p on d.project_id = p.id
WHERE
  d.id = 2;


SELECT
  *
FROM
  document d
JOIN revision r ON r.document_id = d.id
JOIN project p ON d.project_id = p.id
JOIN "user" u ON p.owner_id = u.id
WHERE
  d.id = 2;
