import datetime
import json
import os
import random
from dataclasses import dataclass
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()


@dataclass
class Presentation:
    presenter: str
    company: str
    time_from: datetime.time
    time_to: datetime.time
    title: str
    description: Optional[str]


def get_presentations() -> List[Presentation]:
    "Parses agenda.json file and returns list of more readable data objects."
    agenda = json.loads(
        open(os.path.join(os.path.dirname(__file__), "agenda.json")).read()
    )
    records = agenda["records"]

    results = []

    for record_ in records:
        record = record_["fields"]
        presenter = record["Prelegent"]
        company = record.get("Firma")
        _hour = record["Godzina"].replace(".", ":")
        _time_from, _time_to = _hour.split("-")
        hour_from, minute_from = (int(p) for p in _time_from.split(":"))
        hour_to, minute_to = (int(p) for p in _time_to.split(":"))

        time_from = datetime.time(hour=hour_from, minute=minute_from)
        time_to = datetime.time(hour=hour_to, minute=minute_to)

        title = record["Proponowany tytuł prezentacji"]
        description = record.get("Krótki opis prezentacji")

        results.append(
            Presentation(
                presenter=presenter,
                company=company,
                time_from=time_from,
                time_to=time_to,
                title=title,
                description=description,
            )
        )
    return results


class CustomReponse(HTMLResponse):
    def render(self, content: Presentation) -> bytes:
        from pprint import pformat

        return f"<pre>{pformat(content)}</pre>".encode()


@app.get("/random", response_class=CustomReponse)
async def get_random_presentation() -> Presentation:
    """Returns random presentation at automatyzacja.io.

    Returns:
        Presentation
    """
    presentations = get_presentations()

    return random.choice(presentations)


@app.get("/current", response_class=CustomReponse)
async def get_current_presentation() -> Presentation:
    """Returns ongoing presentation at automatyzacja.io.

    Raises:
        HTTPException: When there's no ongoing presentation_

    Returns:
        Presentation
    """
    presentations = get_presentations()
    now = datetime.datetime.now().time()
    try:
        current = [r for r in presentations if r.time_from <= now < r.time_to][0]
    except IndexError:
        raise HTTPException(status_code=404, detail="There's no ongoing presentation")

    return current


@app.get("/next", response_class=CustomReponse)
async def get_next_presentation() -> Presentation:
    """Returns next presentation which will happen on automatyzacja.io

    Raises:
        HTTPException: When there's no next presentation

    Returns:
        Presentation
    """
    presentations = get_presentations()

    try:
        current = await get_current_presentation()
    except HTTPException:
        return presentations[0]

    next_idx = presentations.index(current) + 1

    if next_idx >= len(presentations):
        raise HTTPException(status_code=404, detail="Current presentation is last one!")

    return presentations[next_idx]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
