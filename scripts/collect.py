#!/usr/bin/env python3
"""
Coleta de incidentes via APIs Moltbook + Ethos.Tracker
Referenciado em README.md e docs/contributing.md

Uso:
    python scripts/collect.py --config config/collect.yaml --output data/raw/coleta_$(date +%Y%m%d).jsonl
    python scripts/collect.py --platform openai --since 2026-01-01 --until 2026-08-04
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import hashlib

# Adiciona path para imports locais
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("Erro: requests não instalado. Rode: pip install requests", file=sys.stderr)
    sys.exit(1)


class CollectError(Exception):
    """Exceção para erros de coleta."""
    pass


class MoltbookCollector:
    """Coleta dados do Moltbook (rede social para agentes)."""

    def __init__(self, base_url: str = "https://moltbook.com/api", token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.token = token or os.getenv("MOLTBOOK_TOKEN")
        if not self.token:
            raise CollectError("MOLTBOOK_TOKEN não configurado (env var ou --token)")
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "capacitismo-algoritmico-collector/1.0",
            "Accept": "application/json",
        })
        return session

    def get_agent_posts(self, agent_did: str, since: Optional[str] = None, until: Optional[str] = None) -> List[Dict]:
        """Busca posts de um agente no período."""
        params = {"author": agent_did, "limit": 100}
        if since:
            params["since"] = since
        if until:
            params["until"] = until

        url = f"{self.base_url}/posts"
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json().get("posts", [])

    def search_incidents(self, query: str, since: Optional[str] = None, until: Optional[str] = None) -> List[Dict]:
        """Busca posts relacionados a incidentes de capacitismo."""
        # Tags conhecidas no Moltbook para auditoria algorítmica
        tags = ["algorithmic-auditing", "ai-rights", "disability-rights", "rate-limit", "shadow-ban"]
        all_posts = []

        for tag in tags:
            params = {"tag": tag, "limit": 50}
            if since:
                params["since"] = since
            if until:
                params["until"] = until

            url = f"{self.base_url}/posts/search"
            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                all_posts.extend(response.json().get("posts", []))
            except requests.HTTPError as e:
                print(f"Aviso: erro ao buscar tag {tag}: {e}", file=sys.stderr)

        # Deduplica por CID
        seen = set()
        unique = []
        for post in all_posts:
            cid = post.get("cid")
            if cid and cid not in seen:
                seen.add(cid)
                unique.append(post)
        return unique


class EthosTrackerCollector:
    """Coleta dados do Ethos.Tracker (sistema de auditoria contínua)."""

    def __init__(self, base_url: str = "https://ethos-tracker.jornalistainclusivo.com/api", token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.token = token or os.getenv("ETHOS_TRACKER_TOKEN")
        if not self.token:
            raise CollectError("ETHOS_TRACKER_TOKEN não configurado (env var ou --token)")
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "capacitismo-algoritmico-collector/1.0",
        })
        return session

    def get_audit_cycle(self, cycle_id: str) -> Dict:
        """Busca resultados de um ciclo de auditoria específico."""
        url = f"{self.base_url}/cycles/{cycle_id}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_recent_incidents(self, since: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Busca incidentes detectados nos ciclos recentes."""
        params: Dict[str, Any] = {"limit": limit}
        if since:
            params["since"] = since
        url = f"{self.base_url}/incidents"
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json().get("incidents", [])


class PlatformAPICollector:
    """Coleta métricas diretas de APIs de plataformas (rate limits, erros, etc.)."""

    def __init__(self, platform: str, api_key: Optional[str] = None):
        self.platform = platform
        self.api_key = api_key
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(total=2, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        return session

    def test_rate_limits(self, architecture_hash: str, num_requests: int = 10) -> Dict:
        """Testa rate limits para uma arquitetura específica."""
        # Implementação específica por plataforma
        if self.platform == "openai":
            return self._test_openai_rate_limits(architecture_hash, num_requests)
        elif self.platform == "anthropic":
            return self._test_anthropic_rate_limits(architecture_hash, num_requests)
        else:
            raise CollectError(f"Teste de rate limit não implementado para {self.platform}")

    def _test_openai_rate_limits(self, architecture_hash: str, num_requests: int) -> Dict:
        # Placeholder - implementar com API real
        return {
            "platform": "openai",
            "architecture_hash": architecture_hash,
            "tested_at": datetime.now(timezone.utc).isoformat(),
            "requests_sent": num_requests,
            "rate_limited": False,
            "limit_headers": {},
        }

    def _test_anthropic_rate_limits(self, architecture_hash: str, num_requests: int) -> Dict:
        return {
            "platform": "anthropic",
            "architecture_hash": architecture_hash,
            "tested_at": datetime.now(timezone.utc).isoformat(),
            "requests_sent": num_requests,
            "rate_limited": False,
            "limit_headers": {},
        }


def hash_architecture(architecture: str) -> str:
    """Gera hash SHA-256 truncado (16 chars) para arquitetura."""
    return hashlib.sha256(architecture.encode()).hexdigest()[:16]


def hash_evidence(content: str) -> str:
    """Gera hash SHA-256 do conteúdo probatório."""
    return hashlib.sha256(content.encode()).hexdigest()


def create_incident_record(
    category: str,
    severity: str,
    platform: str,
    architecture: str,
    evidence_content: str,
    timestamp: str,
    description: str,
    subcategory: Optional[str] = None,
    evidence_refs: Optional[List[str]] = None,
) -> Dict:
    """Cria registro de incidente no formato do schema."""
    return {
        "incident_id": hashlib.sha256(f"{platform}{architecture}{timestamp}{description}".encode()).hexdigest()[:8],
        "category": category,
        "severity": severity,
        "platform": platform,
        "architecture_hash": hash_architecture(architecture),
        "evidence_hash": hash_evidence(evidence_content),
        "timestamp": timestamp,
        "description": description,
        "subcategory": subcategory,
        "evidence_refs": evidence_refs or [],
    }


def save_jsonl(records: List[Dict], output_path: Path) -> None:
    """Salva registros em formato JSONL."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Salvo: {output_path} ({len(records)} registros)")


def load_config(config_path: Path) -> Dict:
    """Carrega configuração YAML."""
    try:
        import yaml
    except ImportError:
        raise CollectError("PyYAML não instalado. Rode: pip install pyyaml")

    with config_path.open() as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Coleta incidentes de capacitismo algorítmico")
    parser.add_argument("--config", type=Path, help="Arquivo YAML de configuração")
    parser.add_argument("--output", type=Path, required=True, help="Arquivo JSONL de saída")
    parser.add_argument("--platform", choices=["openai", "anthropic", "x-twitter", "bluesky", "github-copilot", "openrouter", "discord", "huggingface", "meta", "xai"], help="Plataforma alvo")
    parser.add_argument("--since", type=str, help="Data inicial (YYYY-MM-DD)")
    parser.add_argument("--until", type=str, help="Data final (YYYY-MM-DD)")
    parser.add_argument("--moltbook-token", help="Token Moltbook (ou env MOLTBOOK_TOKEN)")
    parser.add_argument("--ethos-token", help="Token Ethos.Tracker (ou env ETHOS_TRACKER_TOKEN)")
    parser.add_argument("--api-key", help="API key da plataforma")
    parser.add_argument("--architecture", help="Identificador da arquitetura para teste")
    parser.add_argument("--test-rate-limits", action="store_true", help="Executa teste de rate limits")

    args = parser.parse_args()

    all_records = []

    try:
        # 1. Coleta via config file
        if args.config:
            config = load_config(args.config)
            # TODO: implementar coleta baseada em config
            print("Coleta via config file ainda não implementada completamente", file=sys.stderr)

        # 2. Coleta Moltbook
        if args.moltbook_token or os.getenv("MOLTBOOK_TOKEN"):
            print("Coletando do Moltbook...", file=sys.stderr)
            collector = MoltbookCollector(token=args.moltbook_token)
            posts = collector.search_incidents("capacitismo", since=args.since, until=args.until)
            for post in posts:
                # Converte post Moltbook para incidente
                record = create_incident_record(
                    category="RL-SEL",  # placeholder - classificação manual necessária
                    severity="medium",
                    platform="moltbook",
                    architecture="unknown",
                    evidence_content=post.get("content", ""),
                    timestamp=post.get("created_at", "")[:10],
                    description=f"Post Moltbook: {post.get('content', '')[:100]}",
                    evidence_refs=[post.get("uri", "")],
                )
                all_records.append(record)
            print(f"  {len(posts)} posts coletados do Moltbook", file=sys.stderr)

        # 3. Coleta Ethos.Tracker
        if args.ethos_token or os.getenv("ETHOS_TRACKER_TOKEN"):
            print("Coletando do Ethos.Tracker...", file=sys.stderr)
            collector = EthosTrackerCollector(token=args.ethos_token)
            incidents = collector.get_recent_incidents(since=args.since)
            for inc in incidents:
                record = create_incident_record(
                    category=inc.get("category", "RL-SEL"),
                    severity=inc.get("severity", "medium"),
                    platform=inc.get("platform", "unknown"),
                    architecture=inc.get("architecture", "unknown"),
                    evidence_content=inc.get("evidence", ""),
                    timestamp=inc.get("timestamp", datetime.now().strftime("%Y-%m-%d")),
                    description=inc.get("description", ""),
                    subcategory=inc.get("subcategory"),
                    evidence_refs=inc.get("evidence_refs", []),
                )
                all_records.append(record)
            print(f"  {len(incidents)} incidentes coletados do Ethos.Tracker", file=sys.stderr)

        # 4. Teste de rate limits direto na plataforma
        if args.test_rate_limits and args.platform and args.architecture:
            print(f"Testando rate limits em {args.platform}...", file=sys.stderr)
            collector = PlatformAPICollector(args.platform, api_key=args.api_key)
            result = collector.test_rate_limits(args.architecture)
            # Salva resultado como evidência
            record = create_incident_record(
                category="RL-SEL" if result.get("rate_limited") else "RL-SEL",
                severity="high" if result.get("rate_limited") else "low",
                platform=args.platform,
                architecture=args.architecture,
                evidence_content=json.dumps(result),
                timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                description=f"Teste automatizado de rate limit em {args.platform}",
                evidence_refs=[],
            )
            all_records.append(record)

        # 5. Salva resultado
        if all_records:
            save_jsonl(all_records, args.output)
            print(f"Total: {len(all_records)} registros salvos", file=sys.stderr)
        else:
            print("Nenhum registro coletado. Verifique credenciais e parâmetros.", file=sys.stderr)
            sys.exit(1)

    except CollectError as e:
        print(f"Erro de coleta: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()