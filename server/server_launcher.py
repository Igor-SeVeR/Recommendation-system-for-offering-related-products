from typing import Any, Dict

from fastapi import FastAPI, Depends, HTTPException, status
from config import HOST, PORT, PATH_TO_SAVE_DATA, \
    WORD2VEC_FILE_NAME, STOCKCODE_FILE_NAME

import recommendation_system
import users_operations_api
import uvicorn
import utils

app = FastAPI()


def send_to_neuro(data: Dict[str, Any]) -> dict:
    print(data)
    try:
        neuro_result = recommendation_system.get_recommendations(data)
    except:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Incorrect cart format",
            headers={"Cart format": "Incorrect"},
        )
    return neuro_result


@app.post('/send_data')
async def get_recommendation(data: Dict[str, Any],
                             current_user: users_operations_api.User =
                             Depends(users_operations_api.get_current_user)):
    print(current_user)
    if not utils.check_main_hashed_files():
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Model files were changed. Restart the server.",
            headers={"Model files were changed": "Restart the server."},
        )
    res = send_to_neuro(data)
    return {"result": res}


if __name__ == '__main__':
    file_status = utils.check_files(PATH_TO_SAVE_DATA + STOCKCODE_FILE_NAME,
                                    PATH_TO_SAVE_DATA + WORD2VEC_FILE_NAME)
    if not file_status:
        print('Check and fix files. Aborting...')
        exit(0)
    utils.hash_main_files()
    app.include_router(users_operations_api.router)
    uvicorn.run(app, host=HOST, port=PORT)
