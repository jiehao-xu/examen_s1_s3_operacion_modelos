Comandos ejecutados:
    - uv init --package clasificador-paquetes
    - cd clasificador-paquetes
    - uv add pydantic scikit-learn joblib numpy scipy pytest
    - uv run clasificador_paquetes.inference --input <file_name> --output <file_name> --model <file_name>