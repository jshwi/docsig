#!/bin/bash
for i in {1..5}; do
  echo "Checking if version $TAG exists in RTD (attempt $i/5)..."

  EXISTS=$(curl -s -H "Authorization: Token $RTD_TOKEN" \
    "$API/$PROJECT/versions/$TAG/" | jq -r '.slug // empty')

  if [[ "$EXISTS" == "$TAG" ]]; then
    echo "Found version $TAG in RTD. Activating..."

    RES=$(curl -s -o /dev/null -w "%{http_code}" \
      -H "Authorization: Token $RTD_TOKEN" \
      -H "Content-Type: application/json" \
      -X PATCH \
      -d '{"active":true, "hidden":false}' \
      "$API/$PROJECT/versions/$TAG/")

    if [[ "$RES" == "200" || "$RES" == "204" ]]; then
      echo "Successfully activated version $TAG"
      break
    else
      echo "Activation failed with status: $RES"
      exit 1
    fi
  else
    echo "Version $TAG not yet available. Waiting 15s..."
    sleep 15
  fi
done
