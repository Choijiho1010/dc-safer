/** 대응 인력 1명. 실제 명세는 data/sop/personas.yaml 이 원천이다. */
export interface Operator {
  id: string;
  name: string;
  role: string;
  assignedSystems: string[];
}

/** 한 명에게 전파된 지시와 그 진행 상태. */
export interface Dispatch {
  operatorId: string;
  step: number;
  sopSection: string;
  instruction: string;
  status: "대기" | "수신" | "진행" | "보고완료";
  evidenceType: "photo" | "video" | "text";
}
